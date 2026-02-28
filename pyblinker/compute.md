
---

## 1) What current code looks like and what I want

### Reference flow (morphology / `epoch_features.py`)

* `compute()` builds context + plans columns, then loops epochs and delegates one epoch at a time to `_compute_epoch_record()`
* `_compute_epoch_record()` loops `for modality, channels in modality_channels.items():` and calls `_compute_channel_record()` for each channel
* `_compute_channel_record()` builds a per-blink dataframe **once**, then loops styles and writes stats into the epoch record

### Current kinematics flow (`kinematic_features.py`)

Right now `compute()` loops epochs → modality → **style** → channel, and (re)builds `blink_df` inside the style loop for each channel/style combination .
That’s exactly the structural mismatch you’re pointing out.

---

## 2) Target structure for `kinematic_features.py`

### End state: same call graph pattern as morphology

Add these methods to `KinematicBlinkFeatureExtractor` (names mirror the morphology extractor):

1. `_group_channels_by_modality(modality_map) -> Dict[str, List[str]]`
2. `_build_styles_by_modality(modalities, metadata_cols) -> Dict[str, Set[str]]`
3. `_compute_epoch_record(...) -> Dict[str, float]`
4. `_compute_channel_record(...) -> None` (mutates `record`)
5. `_build_blink_df(...) -> pd.DataFrame`  (build once per channel/epoch)
6. `_compute_style_stats_into_record(...) -> None` (style loop lives here)

This matches the morphology pattern: `compute()` delegates to `_compute_epoch_record()` , which loops modalities/channels and calls `_compute_channel_record()` , which loops styles and writes stats .

---

## 3) Step-by-step refactor plan

### Step A — Extract planning helpers (modality + styles)

In `kinematic_features.py`, move the inline dict building into methods:

* **Create** `_group_channels_by_modality()` to replace:

```py
modality_channels = {}
for ch, mod in modality_map.items():
    modality_channels.setdefault(mod, []).append(ch)
```

(this code is currently in `compute()` )

* **Create** `_build_styles_by_modality()` to replace:

```py
styles_by_modality = {}
for mod in set(modality_map.values()):
    styles_by_modality[mod] = _available_styles(ctx.metadata_cols, mod)
```

(also currently in `compute()` )

✅ Acceptance: no behavior change; just moves logic into methods.

---

### Step B — Add `_compute_epoch_record()` (core structural change)

Implement it to match morphology’s epoch-level orchestration:

**Target loop order (same as morphology):**

* epoch → modality → channel → style

So `_compute_epoch_record()` should do:

* initialize `record = {}`
* for each `modality, channels`:

    * `styles = sorted(styles_by_modality.get(modality) or {"base"})`
    * for each `channel_name` in `channels`:

        * call `_compute_channel_record(record=record, ...)`

This matches morphology’s “epoch record first, then modality/channels, then channel record” design .

✅ Acceptance: `compute()` loop becomes tiny and just calls `_compute_epoch_record()` per epoch (like morphology) .

---

### Step C — Add `_build_blink_df()` (compute once per channel/epoch)

Right now, kinematics computes the extended blink dataframe inside the inner loops .

Create:

* `_build_blink_df(metadata_row, signal, sfreq, modality) -> pd.DataFrame`:

    1. `blink_df = _build_kinematic_blink_frame(metadata_row, modality=modality, sfreq=sfreq)`
    2. `blink_df = _compute_extended_kinematic_metrics(blink_df, signal, sfreq, modality=modality)`
    3. return `blink_df`

✅ Acceptance:

* extended metrics are computed *once per channel/epoch* instead of once per channel/style/epoch.
* values should be identical, just less redundant.

---

### Step D — Add `_compute_style_stats_into_record()` (mirror morphology)

Create a method similar to morphology’s per-style aggregator :

Inputs should include:

* `record`, `metadata_row`, `channel_data`, `channel_name`, `epoch_index`, `sfreq`, `n_times`, `modality`, `style`, `blink_df`

Inside it:

1. `windows = _style_windows(metadata_row, modality, style)`
2. Build the metrics list safely:

    * **Important:** don’t mutate a list returned by `metrics_for_style(style)` (current code does `.extend()` ). Use:
    * `style_metrics = list(metrics_for_style(style)) + list(EXTENDED_METRICS)`
3. `per_metric = _compute_metrics_over_windows(... metrics_for_style=style_metrics ...)`
4. `_write_style_stats_into_record(record=record, per_metric=per_metric, blink_df=blink_df, ...)`

✅ Acceptance:

* For every `(epoch, modality, channel, style)`, the same stats columns are written as before.

---

### Step E — Add `_compute_channel_record()` (build blink_df once, loop styles)

This should match the morphology shape exactly :

Inside:

1. `signal = channel_data[channel_name]["raw"][epoch_index]` (same as current blink_df construction usage)
2. `blink_df = self._build_blink_df(...)`
3. for each style in `styles`: call `_compute_style_stats_into_record(...)`

✅ Acceptance:

* All writes happen through `_write_style_stats_into_record()`, same as now, but with cleaner flow.

---

### Step F — Refactor `compute()` to match morphology’s orchestration

Change `compute()` to:

* build `ctx`, `channel_data`, `modality_channels`, `styles_by_modality`, `columns` (same as now, but via helpers)
* loop epochs:

    * `record = self._compute_epoch_record(...)`
    * append to records
* build final dataframe

Morphology uses `frame_from_records(...)` for consistent column/index handling . Kinematics currently uses `pd.DataFrame.from_records(...)` .

**Plan recommendation:**

* Import and use `frame_from_records` for kinematics too (consistency + ensures missing keys become NaN in declared columns, like morphology).
* If `n_epochs == 0` or `columns` empty, return `empty_feature_frame(...)` (already imported but currently unused) .

✅ Acceptance:

* Column set/order remains exactly `build_output_columns(modality_channels, styles_by_modality)`.
* Missing entries are still NaN.

---

## 4) Quick “after” pseudocode (what the final top-level flow should look like)

```py
def compute(...):
    ctx = build_epoch_context(...)
    ch_names, channel_data, index, n_epochs, n_times = prepare_epoch_channel_data(...)

    modality_channels = self._group_channels_by_modality(ctx.modality_by_channel)
    styles_by_modality = self._build_styles_by_modality(set(modality_channels), ctx.metadata_cols)
    columns = build_output_columns(modality_channels, styles_by_modality)

    records = []
    for ei in range(n_epochs):
        metadata_row = get_metadata_row(self.epochs, ei)
        record = self._compute_epoch_record(
            epoch_index=ei,
            metadata_row=metadata_row,
            modality_channels=modality_channels,
            styles_by_modality=styles_by_modality,
            channel_data=channel_data,
            sfreq=ctx.sfreq,
            n_times=n_times,
            n_epochs=n_epochs,
        )
        records.append(record)

    return frame_from_records(records, index=index, columns=columns)
```

That is the same “compute → epoch_record → channel_record” shape as the morphology reference .

---

## 5) Safety checks (to ensure you didn’t change outputs)

1. **Golden test**: run test/run_all_tests.py and ensure all tests pass
