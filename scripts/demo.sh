#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
demo_dir=$(mktemp -d)
trap 'rm -rf "$demo_dir"' EXIT
python3 tasks.py --db "$demo_dir/demo.db" add 'Pay Invoice'
python3 tasks.py --db "$demo_dir/demo.db" add 'Review invoice'
python3 tasks.py --db "$demo_dir/demo.db" add 'Review release'
python3 tasks.py --db "$demo_dir/demo.db" done 1
python3 tasks.py --db "$demo_dir/demo.db" list --search invoice --status open --json
python3 tasks.py --db "$demo_dir/demo.db" list --search absent --json
