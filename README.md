# Legacy Tasks

A deliberately small legacy-style Python/SQLite command-line application.
Requires Python 3.11+; no application dependencies or services to install.

```sh
python3 tasks.py add "Pay invoice"
python3 tasks.py add "Review release"
python3 tasks.py list
python3 tasks.py done 1
python3 tasks.py list --json
python3 -m unittest discover -s tests -v
```

Data persists in `tasks.db` in the working directory. Select another file with
`python3 tasks.py --db /path/to/tasks.db list`. The parent directory must exist.
This is a local single-user demo, not a hosted or multi-user service.

## New feature: search and status filters

```sh
python3 tasks.py list --search invoice
python3 tasks.py list --status open
python3 tasks.py list --search invoice --status done --json
bash scripts/demo.sh
```

Search is a literal Unicode case-insensitive title substring; `%`, `_`, and quotes have no special
meaning. Surrounding whitespace is trimmed and an empty search matches all titles. Search and status
combine with AND. Status defaults to `all`; invalid status exits 2. Empty results succeed.
Results stay in ascending ID order. No database migration is required.

The baseline is commit `dc9f649` on `main`; the feature is on branch `001-task-search` for review.
This is a terminal application. The cloud environment ran its commands and automated tests;
there is no hosted website or long-running service.

- [Feature specification](specs/001-task-search/spec.md)
- [Implementation plan](specs/001-task-search/plan.md)
- [Completed tasks](specs/001-task-search/tasks.md)
- [Verification evidence](specs/001-task-search/verification.md)
- [Spec Kit workflow and reproducibility](docs/workflow.md)

## Continuous verification
[GitHub Actions](https://github.com/rksekar5/Spec-Kit-Remote/actions) runs the tests, virtual demo,
and a pinned Spec Kit CLI smoke test plus artifact audit. Each run uploads logs as artifacts.
See [evidence limits and team workflow](docs/workflow.md#github-actions-added-after-the-initial-pr):
CI does not replay or retroactively prove the original Codex agent skill execution.

## Issue-driven implementation
A maintainer can add `agent-ready` to a reviewed feature or bug issue to start GitHub Copilot through
GitHub Agentic Workflows. It follows the installed Spec Kit instructions, tests the changes, and
creates a draft PR for human review. No model API key is required; eligible Copilot access is required.
See [setup, limits, and the first pilot](docs/issue-automation.md).
