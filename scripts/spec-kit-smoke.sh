#!/usr/bin/env bash
# Runs actual Spec Kit shell commands, not agent prompts. Never rewrites source specs.
set -euo pipefail
repo_root=$(cd "$(dirname "$0")/.." && pwd)
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cp -R "$repo_root/.specify" "$smoke_dir/.specify"
cp -R "$repo_root/.agents" "$smoke_dir/.agents"
cp -R "$repo_root/specs" "$smoke_dir/specs"
cd "$smoke_dir"
git init -q
export SPECIFY_FEATURE_DIRECTORY=specs/001-task-search
export SPECIFY_FEATURE_NO_PERSIST=1
# Trace public commands only. No secrets or environment dumps.
set -x
specify init --here --force --integration codex --ignore-agent-tools --non-interactive
specify check
.specify/scripts/bash/resolve-template.sh constitution-template --json
.specify/scripts/bash/resolve-template.sh spec-template --json
.specify/scripts/bash/check-prerequisites.sh --json --paths-only
# setup-plan overwrites plan.md, hence the disposable copy and restoration below.
cp specs/001-task-search/plan.md original-plan.md
.specify/scripts/bash/setup-plan.sh --json
cp original-plan.md specs/001-task-search/plan.md
.specify/scripts/bash/setup-tasks.sh --json
.specify/scripts/bash/check-prerequisites.sh --json --template checklist-template
.specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
