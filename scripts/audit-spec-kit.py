"""Check artifact structure/completion, not semantic correctness or past agent execution."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FEATURE = ROOT / 'specs/001-task-search'
SKILLS = ('constitution', 'specify', 'clarify', 'plan', 'checklist', 'tasks', 'analyze', 'implement', 'converge')


def require(condition, message):
    if not condition:
        raise SystemExit(f'FAIL: {message}')
    print(f'PASS: {message}')


for name in SKILLS:
    path = ROOT / f'.agents/skills/speckit-{name}/SKILL.md'
    require(path.is_file() and path.stat().st_size > 0, f'installed skill: {name}')
for name in ('spec.md', 'plan.md', 'research.md', 'data-model.md', 'contracts/cli.md',
             'quickstart.md', 'tasks.md', 'verification.md'):
    path = FEATURE / name
    require(path.is_file() and path.stat().st_size > 0, f'feature artifact: {name}')
    require('NEEDS CLARIFICATION' not in path.read_text(), f'no unresolved clarification: {name}')
tasks = (FEATURE / 'tasks.md').read_text()
entries = re.findall(r'^- \[([ xX])\] (T\d+)\b', tasks, re.M)
require(bool(entries), 'task list is not empty')
require(all(mark.lower() == 'x' for mark, _ in entries), 'all task markers are completed')
require(len({task_id for _, task_id in entries}) == len(entries), 'task IDs are unique')
for path in sorted((FEATURE / 'checklists').glob('*.md')):
    marks = re.findall(r'^- \[([ xX])\]', path.read_text(), re.M)
    require(bool(marks) and all(mark.lower() == 'x' for mark in marks), f'completed review: {path.name}')
spec = (FEATURE / 'spec.md').read_text()
require(len(set(re.findall(r'\*\*(FR-\d+)\*\*', spec))) == 9, 'nine identified functional requirements')
require(len(set(re.findall(r'\*\*(SC-\d+)\*\*', spec))) == 3, 'three identified success criteria')
require(subprocess.run(['git', 'diff', '--exit-code'], cwd=ROOT, capture_output=True).returncode == 0,
        'CLI smoke left tracked files unchanged')
print('Structural audit complete. Semantic convergence and historical skill execution are not proven by this audit.')
