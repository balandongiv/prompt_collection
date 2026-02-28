# Instruction for the Refactoring Agent

You are performing a major refactor of the pyblinker codebase. The refactor must follow the strategy and phases defined in `major_refactor_plan.md`  (the plan content provided in `major_refactor_plan.md`). Treat this plan as the single source of truth for what to change and in what order.

## 1) Mandatory reference plan and progress tracking

Use `major_refactor_plan.md` as a living checklist throughout the work.
For every actionable item / phase in the plan:

* Convert it into a checklist item if it is not already formatted as one.
* Mark the item with a right tick (✔) only when:

    * the refactor work for that item is fully complete, and
    * all tests pass (see Testing constraints below).
* Add a brief audit note next to each completed ✔ item stating:

    * what changed (high-level),
    * where it changed (modules/files),
    * any relevant migration notes (if applicable).

If an item remains incomplete, leave it unticked and add a short note explaining why it is pending.

Progress marking must be done inside the plan file itself `major_refactor_plan.md`.

## 2) Non-negotiable testing constraints

Do not modify** `test/run_all_tests.py` or any unit test files.
After each meaningful refactor step (and обязательно before ticking anything in the plan), run:

* `python test/run_all_tests.py`

The refactor step is acceptable only if all 49 tests pass with no errors.

## 3) Behavioral safety and compatibility

Phase 1 items are explicitly “safe refactors (no behaviour change)”; preserve behavior and public output formats unless the plan explicitly authorizes change.

Maintain compatibility, especially around:

* feature column naming conventions,
* default configuration values,
* optional dependencies behavior (tests must still run when optional packages are missing, as the plan describes).

## 4) Working method (how to execute)

Implement refactor items in the order suggested by the plan unless a dependency requires reordering.

Keep changes small and testable:

* complete a single plan item (or a tightly scoped sub-step),
* run the full test suite,
* only then tick ✔ and annotate.

If a plan item requires introducing new modules, shared helpers, configuration objects, or consolidation logic, do so in a way that:

* reduces duplication,
* centralizes configuration
* introduces shared compute orchestration where specified,
* preserves existing behavior and test expectations.
* Do not create or call “thin wrappers” (functions that add no logic beyond renaming/forwarding parameters). This includes _private helpers that simply call another function. Replace them with direct calls to the underlying implementation (prefer public APIs), keeping semantics unchanged.
## Must do, no negotiation:
* must implement the `Design proposal: shared compute skeleton` as describe in `major_refactor_plan.md`
## 5) Definition of done

The refactor is complete only when:

* Every plan item is either:

    * completed and marked ✔ with an audit note and tests passing, or
    * left unticked with a brief note explaining why it remains pending.
* `python test/run_all_tests.py` finishes successfully with all 49 tests passing.
* The refactor achieves the plan’s goals (e.g., reduced duplication, centralized config, shared helpers, unified compute skeleton) while maintaining compatibility and coverage.

Do not claim completion of any plan item unless it is ticked ✔ in the plan and the full test run has passed immediately beforehand.
