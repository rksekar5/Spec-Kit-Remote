# Issue to PR using your ChatGPT/Codex subscription

## Current workflow
1. Create a feature or bug issue using the repository templates.
2. Start Codex, sign in with your ChatGPT account, connect this repository, and provide the issue URL.
3. Ask Codex to follow the installed Spec Kit skills, implement the issue on a new branch, run tests,
   and open a PR. Use `specs/issue-N/` for the feature's specification and execution evidence.
4. Review the PR and GitHub Actions results, then merge it yourself.

Example prompt:
> Implement https://github.com/rksekar5/Spec-Kit-Remote/issues/4 using the installed Spec Kit workflow.
> Record actual commands and test results under specs/issue-4/, preserve existing behavior, and open
> a PR for human review. Do not merge it.

The human starts the task in Codex. Adding `agent-ready` to an issue is no longer an agent trigger.
No model API key is required in GitHub. Codex usage follows your ChatGPT plan and its limits.
The repository's Actions workflow runs tests and Spec Kit shell/artifact checks; it does not invoke
Codex, replay the chat, or independently prove all agent reasoning stages.

## Spec Kit execution
Read the existing constitution and installed skills at `.agents/skills/speckit-*/SKILL.md`.
Follow specify, clarify, plan, checklist/review, tasks, analyze, implement and converge; review
constitution compliance without rewriting it unless the task calls for an amendment.
Run real test commands and preserve initial failures for meaningful new tests. There is no separate
installed verify skill; validation uses the test suite and convergence review.

Application checks:
```sh
python3 -m unittest discover -s tests -v
bash scripts/demo.sh
```
The existing Actions workflow provides reproducible logs for these checks. The feature execution
record must distinguish shell results from judgments made by the Codex agent.

## Why the Copilot workflow was retired
The first live run failed before model execution:
https://github.com/rksekar5/Spec-Kit-Remote/actions/runs/42908558865
The Copilot models endpoint returned HTTP 403: `unauthorized: not authorized to use this Copilot feature`.
Your ChatGPT subscription does not grant GitHub Copilot entitlement. We disabled the workflow and
removed its active source/generated YAML and compiler-only CI job. Historical code and logs remain
in Git history and Actions. Repository verification continues normally.

The `agent-ready` label may be kept as a planning label, but it has no automation semantics here.
Automatic issue-label-to-code generation would need a separate supported agent authentication and
billing setup. We are using subscription-backed Codex tasks instead.
