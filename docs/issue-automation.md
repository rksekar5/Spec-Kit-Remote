# Issue to PR with GitHub Copilot — no model API key

## What runs
A maintainer adds `agent-ready` to an open feature or bug issue. GitHub Actions runs the compiled
GitHub Agentic Workflow, which uses Copilot inference through its short-lived `GITHUB_TOKEN` and
`copilot-requests: write`. No Anthropic/OpenAI key or personal access token is required by this design.
This still requires eligible Copilot access and available usage/billing for the repository owner;
GitHub Actions minutes and Copilot usage are not necessarily free.

Source: `.github/workflows/issue-to-pr.md`.
Executable generated workflow: `.github/workflows/issue-to-pr.lock.yml`.
Compiler: GitHub's `gh-aw` v1.2.2. Do not hand-edit the generated file.

## Enable and pilot
1. Merge the automation PR after reviewing its successful validation checks. Issue events use workflows
   on the default branch; the feature branch alone does not activate this pipeline.
2. Confirm your GitHub account has eligible Copilot access. If a run reports a licensing or billing
   error, resolve it in GitHub Copilot settings; do not add a model API key.
3. In repository Settings → Actions → General, allow GitHub Actions to create pull requests, if that
   option is disabled. Policy may also need to permit the pinned GitHub Agentic Workflows actions.
4. Create a feature/bug issue using the templates and review its requirements. Add `agent-ready`
   manually as a maintainer. The label is intentionally not applied by the issue templates.
5. Open Actions → Issue to Spec Kit PR. Inspect activation, agent session logs, test evidence,
   threat detection, and guarded publication. An entitlement failure is not a successful implementation.
6. Review the resulting draft PR and its `specs/issue-N/execution.md`.
7. GitHub normally suppresses ordinary CI events caused by `GITHUB_TOKEN`. Run
   `Verify feature and Spec Kit` manually with the generated branch selected; inspect that run's
   commit SHA. An empty check list is not passing CI. Review and merge only after checks pass.

Repository-level Copilot entitlement could not be verified through this chat connection. Its
suggested-assignee API did not advertise the cloud agent; that does not establish CLI entitlement.
A live issue-to-PR pilot remains necessary after merge. No model execution is claimed by the compiler
or existing smoke-test jobs.

## Spec Kit execution
Copilot reads the actual installed `.agents/skills/speckit-*/SKILL.md` files and performs the stages.
The prompt requires constitution compliance, specify, clarify, plan, checklist generation and review,
tasks, analyze, implement, actual tests, and converge. It runs the helpers prescribed by those skills.
The constitution is already adopted; this workflow does not authorize changing governance.

Each issue has `specs/issue-N/`, with real test outputs and a stage ledger. Bugs require reproduction
and regression evidence. Essential ambiguity produces a blocker comment. Convergence permits at most
two remediation rounds. No separate `speckit-verify` command is invented.

These stage requirements are agent instructions, not a deterministic nine-stage state machine.
Review session logs and evidence; the PR remains a draft for a human to assess. The existing
Spec Kit shell smoke/audit CI is distinct from this workflow's actual Copilot execution.

## Enforced controls and limits
- Only admin, maintainer, or write-role actors can trigger the agent; other label events are skipped.
- Only the `agent-ready` label on open issues triggers the workflow.
- Runs are serialized per issue. Search skips existing PRs from the exact deterministic branch,
  including closed PRs. Fixed branch names and no force replacement further prevent duplicates.
- One draft PR per run, targeting main; no automatic merge or approval capability.
- Publication is restricted to tasks.py, tests, specs, docs, and README.md. Changes to workflows,
  credentials, skills, governance and other paths are refused. Ask for a human-owned PR for those.
- The agent has read-only repository access. GitHub's safe-output jobs apply permitted mutations
  separately; the agent runs within the framework's network sandbox and threat checks.
- Agent runtime: 45 minutes, at most 100 turns and 300 AI Credits. The framework's credit estimate is
  not a contractual bill cap. Threat detection and GitHub Actions compute can have additional costs.
- Existing PRs suppress repeated implementation. Continue review on the existing PR; this first
  version does not automatically revise PRs from review comments.
- Removing the label does not cancel an already-running job. Cancel it from Actions if needed.
- Repeated labels before a PR exists can retry failed work; there is no automatic retry loop.

Timeouts, quota exhaustion, authentication errors and tool failures appear in the Actions run.
The agent is instructed to comment for actionable blockers, but a hard timeout can prevent a comment.

## Maintenance and validation
```sh
gh extension install github/gh-aw --pin v1.2.2
gh aw compile issue-to-pr --validate
python3 -m unittest discover -s tests -v
bash scripts/demo.sh
```
Commit the Markdown source, lock YAML and `.github/aw/actions-lock.json` together. CI recompiles and
fails if the generated files drift. No model call or model credentials are needed for compilation.

## Official references
- [Copilot authentication and personal-repository billing](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/copilot-cli-in-github-actions)
- [Using the built-in Actions token](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-in-actions)
- [GitHub Agentic Workflows](https://github.github.com/gh-aw/setup/quick-start/)
- [Guarded pull request publication](https://github.github.com/gh-aw/reference/safe-outputs-pull-requests/)
