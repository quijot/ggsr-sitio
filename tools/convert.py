#!/usr/bin/env python3
"""Convert Nikola RST/Textile pages to Hugo Markdown content."""
import re
import subprocess
from pathlib import Path

SITE_ROOT = Path('/home/santi/devel/ggsr_site')
PAGES_DIR = SITE_ROOT / 'pages'
OUTPUT_DIR = Path('/home/santi/devel/ggsr_hugo/content')

META_RE = re.compile(r'^\.\.\s+([\w-]+):\s*(.*)')

KNOWN_META = {
    'title', 'slug', 'date', 'tags', 'link', 'description', 'type', 'template', 'status',
}


def extract_meta(text: str) -> tuple[dict, str]:
    lines = text.splitlines(keepends=True)
    meta = {}
    i = 0
    for i, line in enumerate(lines):
        m = META_RE.match(line)
        if m and m.group(1).lower() in KNOWN_META:
            meta[m.group(1).lower()] = m.group(2).strip()
        else:
            break
    # Skip blank lines after metadata block
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    return meta, ''.join(lines[i:])


def parse_date(s: str) -> str:
    if not s:
        return ''
    m = re.match(r'(\d+)/(\d+)/(\d+)', s)
    if not m:
        return s
    a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
    # Disambiguate DD/MM/YY vs MM/DD/YY
    if a > 12:               # a must be day
        day, month, year = a, b, c
    elif b > 12:             # b must be day
        month, day, year = a, b, c
    else:                    # ambiguous — treat as MM/DD/YY (Nikola default)
        month, day, year = a, b, c
    year = 2000 + year if year < 100 else year
    return f'{year:04d}-{month:02d}-{day:02d}'


def make_frontmatter(meta: dict) -> str:
    lines = ['---']
    if 'title' in meta:
        lines.append(f'title: "{meta["title"].replace(chr(34), chr(92)+chr(34))}"')
    if 'slug' in meta:
        lines.append(f'slug: "{meta["slug"]}"')
    date = parse_date(meta.get('date', ''))
    if date:
        lines.append(f'date: {date}')
    if meta.get('template') in ('notitle.tmpl',):
        lines.append('notitle: true')
    lines.append('---')
    return '\n'.join(lines)


def inline_includes(rst: str) -> str:
    def replacer(m):
        path = m.group(1).strip()
        for base in (SITE_ROOT, PAGES_DIR):
            full = base / path
            if full.exists():
                return full.read_text()
        return f'.. note:: [include not found: {path}]\n'
    return re.sub(r'^\.\. include::\s*(.+)$', replacer, rst, flags=re.MULTILINE)


def pandoc(text: str, from_fmt: str) -> str:
    result = subprocess.run(
        ['docker', 'run', '--rm', '-i', 'pandoc/core',
         '-f', from_fmt, '-t', 'gfm', '--wrap=none'],
        input=text, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f'  [pandoc error] {result.stderr[:300]}')
    return result.stdout if result.stdout else text


def convert(src: Path):
    text = src.read_text()
    meta, body = extract_meta(text)

    fmt = 'rst' if src.suffix in ('.txt', '.md') else 'textile'

    if fmt == 'rst':
        body = inline_includes(body)

    md_body = pandoc(body, fmt)

    slug = meta.get('slug', src.stem)
    fm = make_frontmatter(meta)

    if slug == 'index':
        out = OUTPUT_DIR / '_index.md'
    else:
        out = OUTPUT_DIR / f'{slug}.md'

    out.write_text(fm + '\n\n' + md_body)
    print(f'  {src.name} → {out.name}')


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sources = (
        [p for p in sorted(PAGES_DIR.glob('*.txt')) if not p.stem.endswith('_')]
        + [p for p in sorted(PAGES_DIR.glob('*.textile')) if not p.stem.endswith('_')]
        + [p for p in sorted(PAGES_DIR.glob('*.md')) if not p.stem.endswith('_')]
    )
    for src in sources:
        print(f'Converting {src.name}...')
        convert(src)
    print('\nDone.')


if __name__ == '__main__':
    main()
