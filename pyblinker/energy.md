Below is a refactor plan for **`energy_features.py`** that makes its top-level flow match the *morphology reference* (`epoch_features.py`):

**`compute()` → `record = _compute_epoch_record(...)` → `for modality, channels in modality_channels.items():` → `_compute_channel_record(...)`** (and then style/stat writing happens inside the channel record), like the reference’s `_compute_channel_record()` structure .

---

## 0) Current energy flow (what to change)

Right now `compute_energy_features(...)` loops **epoch → channel**, and inside each channel computes `style_windows_from_metadata(...)`, computes stats, then writes into `record` . That means:

* There’s **no `_compute_epoch_record()`** concept.
* You’re **not looping by modality first**.
* You recompute **style windows once per channel**, even though windows depend only on `(epoch metadata, modality, n_times)`.

---

## 1) Target flow (match `epoch_features.py` reference)

Keep the public API `compute_energy_features(epochs, picks=None)`, but refactor internally into helpers mirroring the reference call graph:

### New helper functions to add (module-level)

1. `_group_channels_by_modality(modality_by_channel, ch_names) -> Dict[str, List[str]]`
2. `_compute_epoch_record(...) -> Dict[str, float]`
3. `_compute_channel_record(...) -> None`  (mutates `record`)
4. `_write_energy_style_stats_into_record(...) -> None` (mutates `record`)
5. (optional but recommended) `_compute_style_windows_for_modality(...) -> Dict[str, List[tuple[int,int]]]`

This matches the morphology pattern where `_compute_epoch_record()` delegates down to `_compute_channel_record()` which then loops styles and writes stats .

---

## 2) Step-by-step refactor plan

### Step A — Build `modality_channels` once (like reference)

Add:

* `_group_channels_by_modality(ctx.modality_by_channel, ctx.ch_names)`

So you can loop `for modality, channels in modality_channels.items():` (the pattern you want).

This addresses the structural mismatch: energy currently iterates `for ci, ch in enumerate(ctx.ch_names): modality = ...` .

✅ Acceptance: no output change yet; just enabling the target loop order.

---

### Step B — Introduce `_compute_epoch_record(...)`

Create:

* `_compute_epoch_record(*, epoch_index, metadata_row, ctx, modality_channels, styles_by_modality, available_raw_styles, data, ch_to_ci) -> Dict[str, float]`

Implementation outline:

* `record = {}`
* loop `for modality, channels in modality_channels.items():`

    * compute **style windows once per epoch+modality** (see Step C)
    * loop channels and call `_compute_channel_record(...)`
* return `record`

This gives you the same “epoch record first” structure as the reference (`record = ...` then deeper loops) .

✅ Acceptance: `compute_energy_features()` becomes a thin orchestration loop over epochs.

---

### Step C — Move style-window creation up to epoch+modality level (important improvement)

Right now, windows are created inside the channel loop  even though windows don’t depend on channel signal.

Refactor so `_compute_epoch_record()` does:

* `windows_by_style = style_windows_from_metadata(metadata_row=..., modality=..., available_styles=..., n_times=..., include_half=True, include_peak=True, ear_mode="keep")`

Then pass `windows_by_style` into `_compute_channel_record(...)`.

✅ Acceptance:

* Same windows as before, but computed **once per modality per epoch**, not once per channel.

**Also fix potential style-key mismatch**
You normalize styles for columns with `_normalize_styles_for_modality(...)` , but windows are computed using `available.get(modality, set())` (raw) . To ensure the record only writes keys that exist in `columns`, do one of:

* Filter `windows_by_style` to `normalized_styles = styles_by_modality.get(modality, set())`, OR
* Map/merge raw styles into the normalized style names before stats.

(Otherwise you risk computing/writing a style that isn’t in `columns` and it gets dropped by `frame_from_records(..., columns=columns)` .)

---

### Step D — Add `_compute_channel_record(...)` (channel-level work, like reference)

Create:

* `_compute_channel_record(*, record, epoch_index, modality, channel_name, signal_1d, windows_by_style, sfreq, n_times) -> None`

Inside:

1. `stats_by_style = _compute_epoch_channel_energy_stats(style_windows=windows_by_style, signal_1d=signal_1d, sfreq=sfreq, n_times=n_times)`
2. Loop `for style, style_metrics in stats_by_style.items(): ...` and delegate writing to `_write_energy_style_stats_into_record(...)`

This mirrors the reference idea: channel-level function does the heavy lift, then loops styles and writes into `record` .

✅ Acceptance: outputs identical; only responsibilities move.

---

### Step E — Extract record-writing into `_write_energy_style_stats_into_record(...)`

Right now, record-writing is a deep nested loop inside `compute_energy_features()` .

Move it into:

* `_write_energy_style_stats_into_record(record, modality, style, channel_name, style_metrics)`

It should encapsulate the existing key naming logic:

* `make_stat_column(modality=..., style=..., metric=..., stat=..., channel=ch if modality=="eog" else ch.upper())`

✅ Acceptance: identical column names/values.

---

### Step F — Rewrite `compute_energy_features(...)` orchestration to match reference

After the refactor, `compute_energy_features(...)` should look like:

* build ctx, available styles, normalized styles, columns (as it does today)
* precompute:

    * `modality_channels = _group_channels_by_modality(...)`
    * `data = epochs.get_data(picks=ctx.ch_names)`
    * `ch_to_ci = {ch: i for i, ch in enumerate(ctx.ch_names)}`
* loop epochs:

    * `metadata_row = get_metadata_row(epochs, ei)`
    * `record = _compute_epoch_record(...)`
* `df = frame_from_records(records, index=ctx.index, columns=columns)` (already used)

Also: you import `empty_feature_frame` but don’t use it . Add an early return for `ctx.n_epochs == 0` or empty `columns` to match the rest of the feature modules’ behavior.

✅ Acceptance: `compute_energy_features` becomes the same “thin coordinator” style as the morphology reference.

---

## 3) “After” pseudocode (target shape)

```python
def compute_energy_features(...):
    ctx = build_epoch_context(...)
    available_raw = available_styles_by_modality(...)
    styles_by_modality = {mod: _normalize_styles_for_modality(raw, mod) ...}
    columns = build_output_columns(ctx.modality_by_channel, styles_by_modality)

    if ctx.n_epochs == 0 or not columns:
        return empty_feature_frame(index=ctx.index, columns=columns)

    modality_channels = _group_channels_by_modality(ctx.modality_by_channel, ctx.ch_names)
    data = epochs.get_data(picks=ctx.ch_names)
    ch_to_ci = {ch: i for i, ch in enumerate(ctx.ch_names)}

    records = []
    for ei in range(ctx.n_epochs):
        metadata_row = get_metadata_row(epochs, ei)
        record = _compute_epoch_record(
            epoch_index=ei,
            metadata_row=metadata_row,
            ctx=ctx,
            modality_channels=modality_channels,
            styles_by_modality=styles_by_modality,
            available_raw=available_raw,
            data=data,
            ch_to_ci=ch_to_ci,
        )
        records.append(record)

    return frame_from_records(records, index=ctx.index, columns=columns)
```

---

## 4) Output-safety checks (so you don’t accidentally change results)

1. **Golden compare** old vs new:

    * same columns (including order), same index, values equal (NaN-safe).
2. Verify style filtering:

    * for each modality, every style you write exists in `columns` (prevent silent drops).
3. Performance sanity:

    * confirm `style_windows_from_metadata(...)` is called **once per epoch per modality** (not per channel).

---
