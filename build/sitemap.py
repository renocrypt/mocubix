#!/usr/bin/env python3
"""Write the site's two maps from the pages that exist, every site/**/index.html: site/sitemap.xml for crawlers and
site/llms.txt for language models, each page with its description and the folder of the repository it is served
from. On the way, check that every page links to that folder, on the page and in its structured data."""
import datetime, html, json, pathlib, re
SITE = pathlib.Path(__file__).resolve().parent.parent / 'site'
BASE = 'https://mocubix.renocrypt.com/'
REPO = 'https://github.com/renocrypt/mocubix'

pages, urls, wrong = {}, [], []
for p in sorted(SITE.rglob('index.html')):
    rel = p.parent.relative_to(SITE).as_posix()
    path = '' if rel == '.' else f'{rel}/'
    s, source = p.read_text(), f'{REPO}/tree/main/site/{path}'
    urls.append(f'  <url><loc>{BASE}{path}</loc><lastmod>{datetime.date.fromtimestamp(p.stat().st_mtime).isoformat()}</lastmod></url>')
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', s)
    if f'class="source" href="{source}"' not in s or not ld or json.loads(ld[1])['isBasedOn']['url'] != source:
        wrong.append(path or '/')
    kind = ('showcase' if (p.parent / 'showcase.css').exists() else 'pillar' if 'class="pillarhead"' in s
            else 'term' if 'class="termgrid"' in s else 'page')
    name = re.sub(r' — Mocubix( Lexicon)?$', '', html.unescape(re.search(r'<title>(.*?)</title>', s)[1]))
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', s)[1])
    pages[path] = (name, desc, source, kind)
if wrong:
    raise SystemExit(f'no source link, or one to another folder: {", ".join(wrong)}')
(SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')


def linked(page, pattern):
    """The folders a page links to, in its own order."""
    return list(dict.fromkeys(re.findall(pattern, (SITE / page).read_text())))


def entry(path):
    name, desc, source, kind = pages[path]
    return f'- [{name}]({BASE}{path}): {desc}{" A full showcase." if kind == "showcase" else ""} Source: {source}'


terms = sum(1 for p in pages.values() if p[3] in ('term', 'showcase'))
out = ['# Mocubix', '',
       f'> Seven ways a page can move, and a lexicon of {terms} named interface effects, each one running on real material. '
       'Plain HTML and CSS with a few small scripts, no framework, made for Chrome.', '',
       f'Each page is served from its own folder of the repository: {BASE}<path>/ from {REPO}/tree/main/site/<path>/, '
       'and every file there reads as served at https://raw.githubusercontent.com/renocrypt/mocubix/main/site/<path>/<file>. '
       'All pages share site/house.css and site/house.js; the Lexicon adds site/lexicon/lexicon.css and lexicon.js. '
       'A showcase keeps everything else beside its page: index.html, showcase.css and, where it needs one, showcase.js.', '',
       f'The code is licensed under the Apache License 2.0 ({REPO}/blob/main/LICENSE). '
       'The pictures keep their own licences from Wikimedia Commons, credited on each page.', '',
       '## Exhibits', '', entry('')]
out += [entry(p) for p in linked('index.html', r'<a class="card[^"]*" href="([a-z0-9-]+/)"')]
out += ['', '## The Lexicon', '', entry('lexicon/')]
for p in linked('lexicon/index.html', r'<a href="([a-z0-9-]+/)"'):
    path = f'lexicon/{p}'
    if pages[path][3] == 'pillar':
        out += ['', f'### {pages[path][0]}', '']
    out.append(entry(path))
out += ['', '## Optional', '',
        f'- [AGENTS.md]({REPO}/blob/main/AGENTS.md): the laws the site is built by, a map of the repository and its build tools',
        f'- [Traps]({REPO}/blob/main/notes/TRAPS.md): what has already gone wrong once, one line each, with the way out']
listed = sum(1 for line in out if line.startswith('- [') and BASE in line)
assert listed == len(pages), f'llms.txt lists {listed} of {len(pages)} pages'
(SITE / 'llms.txt').write_text('\n'.join(out) + '\n')
print(f'sitemap: {len(urls)} addresses; llms.txt: {listed} pages, every one linked to its source')
