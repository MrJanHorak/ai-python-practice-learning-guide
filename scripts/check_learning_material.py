"""Check maintained local Markdown links and Python syntax; no network calls."""
import ast
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
documents = [ROOT / 'README.md', ROOT / 'VERIFICATION.md']
documents += list((ROOT / 'lessons').glob('*.md')) + list((ROOT / 'guides').glob('*.md')) + list((ROOT / 'data').rglob('*.md'))
errors, links, blocks = [], 0, 0
for path in documents:
    text = path.read_text(encoding='utf-8')
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:|#', target):
            continue
        relative = unquote(target.split('#')[0])
        if relative and not (path.parent / relative).exists():
            errors.append(f'{path.relative_to(ROOT)}: missing {target}')
        links += 1
    for block in re.findall(r'```python\s*\n(.*?)```', text, re.S):
        try:
            ast.parse(block)
        except SyntaxError as error:
            errors.append(f'{path.relative_to(ROOT)}: Python block: {error}')
        blocks += 1
sources = [p for folder in ('examples', 'scripts', 'tests', 'tutorials') for p in (ROOT / folder).rglob('*.py')]
for path in sources:
    try:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    except SyntaxError as error:
        errors.append(str(error))
for error in errors:
    print(error)
print(f'{len(documents)} Markdown files; {links} local links; {blocks} Python blocks; {len(sources)} Python files; {len(errors)} errors')
raise SystemExit(bool(errors))
