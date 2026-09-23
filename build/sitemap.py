#!/usr/bin/env python3
"""Write site/sitemap.xml from the pages that exist: every site/**/index.html."""
import datetime, pathlib
SITE = pathlib.Path(__file__).resolve().parent.parent / 'site'
BASE = 'https://mocubix.renocrypt.com/'
pages = sorted(p.parent.relative_to(SITE).as_posix() for p in SITE.rglob('index.html'))
urls = []
for rel in pages:
    loc = BASE if rel == '.' else f'{BASE}{rel}/'
    day = datetime.date.fromtimestamp((SITE / rel / 'index.html').stat().st_mtime).isoformat()
    urls.append(f'  <url><loc>{loc}</loc><lastmod>{day}</lastmod></url>')
(SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')
print(f'sitemap: {len(urls)} addresses')
