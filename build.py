#!/usr/bin/env python3
"""Builds the two self-contained pages (index.html and admin/index.html).
Each built page has its CSS and JavaScript inside it, so the site still works
even if the assets folder is not uploaded. Run:  python3 build.py
Edit the files in src/ and assets/, then run this, then commit and push."""
import re, os
ROOT = os.path.dirname(os.path.abspath(__file__))

def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()

def inline(src, out):
    html = read(src)
    def css(m):
        return '<style>\n' + read(m.group(1).replace('../', '')) + '\n</style>'
    def js(m):
        code = read(m.group(1).replace('../', ''))
        return '<script>\n' + code.replace('</script', '<\\/script') + '\n</script>'
    html = re.sub(r'<link rel="stylesheet" href="((?:\.\./)?assets/css/[^"]+)">', css, html)
    html = re.sub(r'<script src="((?:\.\./)?assets/js/[^"]+)"></script>', js, html)
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('built', out, len(html) // 1024, 'KB')

inline('src/index.src.html', 'index.html')
inline('src/admin.src.html', 'admin/index.html')
