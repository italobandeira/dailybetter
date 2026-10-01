"""Generates blog pages (PT + EN), sitemap.xml and robots.txt.

Run from the repository root: python tools/build_blog.py
"""
import json
import math
import re

import site_chrome as S
from posts import POSTS

MONTHS_PT = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

B = {
    'pt': {
        'blog_title': 'Blog do DailyBetter — Dicas sobre diário de humor e autoconhecimento',
        'blog_desc': 'Dicas práticas para começar e manter um diário de humor, entender seus padrões e aproveitar melhor o DailyBetter.',
        'blog_eyebrow': 'Blog do DailyBetter',
        'blog_h1': 'Dicas para entender melhor os seus dias.',
        'blog_lead': 'Guias práticos sobre diário de humor, hábitos de registro e como aproveitar o DailyBetter.',
        'read': 'Ler artigo', 'min': 'min de leitura', 'by': 'Por Italo Bandeira',
        'crumb_aria': 'Navegação estrutural', 'home': 'Início',
        'cta_h': 'Comece seu diário de humor hoje.',
        'cta_p': 'O DailyBetter é grátis, não pede cadastro e guarda seus registros no seu celular.',
        'cta_btn': 'Baixar no Google Play',
        'related': 'Leia também', 'list_aria': 'Artigos',
    },
    'en': {
        'blog_title': 'DailyBetter Blog — Mood journaling tips and self-awareness',
        'blog_desc': 'Practical tips for starting and keeping a mood journal, understanding your patterns and getting the most out of DailyBetter.',
        'blog_eyebrow': 'DailyBetter Blog',
        'blog_h1': 'Tips for understanding your days.',
        'blog_lead': 'Practical guides on mood journaling, logging habits and getting the most out of DailyBetter.',
        'read': 'Read article', 'min': 'min read', 'by': 'By Italo Bandeira',
        'crumb_aria': 'Breadcrumb', 'home': 'Home',
        'cta_h': 'Start your mood journal today.',
        'cta_p': 'DailyBetter is free, needs no sign-up and keeps your entries on your phone.',
        'cta_btn': 'Get it on Google Play',
        'related': 'Read next', 'list_aria': 'Articles',
    },
}

SPRITE = '''  <svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" aria-hidden="true">
    <symbol id="icon-arrow" viewBox="0 0 24 24"><path d="M4 12h15m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
    <symbol id="icon-play" viewBox="0 0 24 24"><path d="m5 3 15 9-15 9V3Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="m5 3 10 12m-10 6 10-12" fill="none" stroke="currentColor" stroke-width="1.2"/></symbol>
  </svg>'''


def blog_dir(lang):
    return 'blog/' if lang == 'pt' else 'en/blog/'


def fmt_date(iso, lang):
    y, m, d = (int(x) for x in iso.split('-'))
    return f'{d} de {MONTHS_PT[m - 1]} de {y}' if lang == 'pt' else f'{MONTHS_EN[m - 1]} {d}, {y}'


def minutes(html):
    words = len(re.sub(r'<[^>]+>', ' ', html).split())
    return max(1, math.ceil(words / 200))


def esc(text):
    return text.replace('&', '&amp;').replace('"', '&quot;')


def other(lang):
    return 'en' if lang == 'pt' else 'pt'


def page(path, alt_path, lang, title, description, og_type, jsonld, main, extra_meta=''):
    t = S.T[lang]
    r = S.root_rel(path)
    ld = '\n'.join(f'  <script type="application/ld+json">\n{json.dumps(d, ensure_ascii=False, indent=2)}\n  </script>' for d in jsonld)
    return f'''<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#E7EBDD">
  <title>{title}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow">
{S.head_links(path, alt_path)}  <meta name="author" content="Italo Bandeira">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="DailyBetter">
  <meta property="og:locale" content="{t['og_locale']}">
  <meta property="og:locale:alternate" content="{t['og_alt']}">
  <meta property="og:url" content="{S.url(path)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{S.SITE}assets/icon.png">
  <meta name="twitter:card" content="summary">
{extra_meta}{ld}
  <link rel="icon" type="image/png" href="{r}assets/moods/excellent.png">
  <link rel="preload" href="{r}assets/fonts/Nunito.ttf" as="font" type="font/ttf" crossorigin>
  <link rel="stylesheet" href="{r}legal.css">
  <link rel="stylesheet" href="{r}footer.css">
  <link rel="stylesheet" href="{r}blog.css">
</head>
<body>
  <a class="skip-link" href="#conteudo">{t['skip']}</a>

{SPRITE}

{S.header(path, alt_path, 'blog')}

{main}

{S.footer(path, alt_path, 'blog')}
</body>
</html>
'''


def build_index(lang):
    b = B[lang]
    path = blog_dir(lang) + 'index.html'
    alt = blog_dir(other(lang)) + 'index.html'
    r = S.root_rel(path)
    cards = []
    items = []
    for i, post in enumerate(sorted(POSTS, key=lambda p: p['date'], reverse=True), 1):
        p = post[lang]
        cards.append(f'''      <li>
        <article class="post-card">
          <img src="{r}assets/moods/{post['icon']}.png" alt="" width="56" height="56">
          <p class="post-tag">{p['tag']}</p>
          <h2><a href="{p['slug']}.html">{p['title']}</a></h2>
          <p>{p['description']}</p>
          <p class="post-meta"><time datetime="{post['date']}">{fmt_date(post['date'], lang)}</time> · {minutes(p['body'])} {b['min']}</p>
        </article>
      </li>''')
        items.append({'@type': 'ListItem', 'position': i, 'url': S.url(blog_dir(lang) + p['slug'] + '.html'), 'name': p['title']})
    main = f'''  <main id="conteudo">
    <section class="blog-hero" aria-labelledby="titulo">
      <div class="wrap">
        <p class="eyebrow">{b['blog_eyebrow']}</p>
        <h1 id="titulo">{b['blog_h1']}</h1>
        <p class="lead">{b['blog_lead']}</p>
      </div>
    </section>

    <ul class="wrap post-list" aria-label="{b['list_aria']}">
{chr(10).join(cards)}
    </ul>
  </main>'''
    jsonld = [{
        '@context': 'https://schema.org', '@type': 'Blog', 'name': b['blog_eyebrow'], 'url': S.url(path),
        'inLanguage': S.T[lang]['html_lang'], 'description': b['blog_desc'],
        'publisher': {'@type': 'Organization', 'name': 'iFlag'},
    }, {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': items}]
    html = page(path, alt, lang, b['blog_title'], b['blog_desc'], 'website', jsonld, main)
    open(path, 'w', encoding='utf-8', newline='\n').write(html)
    return path


def build_post(post, lang):
    b = B[lang]
    p = post[lang]
    q = post[other(lang)]
    path = blog_dir(lang) + p['slug'] + '.html'
    alt = blog_dir(other(lang)) + q['slug'] + '.html'
    home = S.home_rel(path)
    related = [x for x in POSTS if x['id'] != post['id']]
    rel_items = '\n'.join(
        f'          <li><a href="{x[lang]["slug"]}.html">{x[lang]["title"]}<svg aria-hidden="true"><use href="#icon-arrow"/></svg></a></li>'
        for x in related)
    body = '\n'.join('        ' + line if line else '' for line in p['body'].strip('\n').split('\n'))
    main = f'''  <main id="conteudo">
    <article>
      <header class="blog-hero">
        <div class="wrap">
          <nav class="breadcrumb" aria-label="{b['crumb_aria']}">
            <ol>
              <li><a href="{home}index.html">{b['home']}</a></li>
              <li><a href="index.html">Blog</a></li>
            </ol>
          </nav>
          <p class="eyebrow">{p['tag']}</p>
          <h1>{p['title']}</h1>
          <p class="lead">{p['lead']}</p>
          <p class="post-meta"><time datetime="{post['date']}">{fmt_date(post['date'], lang)}</time> · {minutes(p['body'])} {b['min']} · {b['by']}</p>
        </div>
      </header>

      <div class="article-layout">
        <div class="article-body">
{body}
        </div>

        <aside class="article-cta" aria-labelledby="cta-titulo">
          <h2 id="cta-titulo">{b['cta_h']}</h2>
          <p>{b['cta_p']}</p>
          <a href="{S.PLAY}" target="_blank" rel="noopener noreferrer"><svg aria-hidden="true"><use href="#icon-play"/></svg>{b['cta_btn']}</a>
        </aside>

        <nav class="related" aria-labelledby="related-titulo">
          <h2 id="related-titulo">{b['related']}</h2>
          <ul>
{rel_items}
          </ul>
        </nav>
      </div>
    </article>
  </main>'''
    jsonld = [{
        '@context': 'https://schema.org', '@type': 'BlogPosting',
        'headline': p['title'], 'description': p['description'], 'inLanguage': S.T[lang]['html_lang'],
        'datePublished': post['date'], 'dateModified': post.get('modified', post['date']),
        'mainEntityOfPage': S.url(path), 'image': S.SITE + 'assets/icon.png',
        'author': {'@type': 'Person', 'name': 'Italo Bandeira', 'url': S.url(('en/' if lang == 'en' else '') + 'contact.html')},
        'publisher': {'@type': 'Organization', 'name': 'iFlag'},
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': b['home'], 'item': S.url(('en/' if lang == 'en' else '') + 'index.html')},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': S.url(blog_dir(lang) + 'index.html')},
            {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': S.url(path)},
        ]}]
    meta = (f'  <meta property="article:published_time" content="{post["date"]}">\n'
            f'  <meta property="article:author" content="Italo Bandeira">\n')
    html = page(path, alt, lang, f"{p['title']} — DailyBetter", p['description'], 'article', jsonld, main, meta)
    open(path, 'w', encoding='utf-8', newline='\n').write(html)
    return path, alt


def build_sitemap():
    pairs = [('index.html', 'en/index.html', '2026-09-30'), ('contact.html', 'en/contact.html', '2026-09-30'),
             ('privacy.html', 'en/privacy.html', '2026-09-29'), ('terms.html', 'en/terms.html', '2026-09-09'),
             ('blog/index.html', 'en/blog/index.html', '2026-09-30')]
    for post in POSTS:
        pairs.append((f"blog/{post['pt']['slug']}.html", f"en/blog/{post['en']['slug']}.html", post.get('modified', post['date'])))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for pt, en, mod in pairs:
        for loc in (pt, en):
            out += ['  <url>', f'    <loc>{S.url(loc)}</loc>', f'    <lastmod>{mod}</lastmod>',
                    f'    <xhtml:link rel="alternate" hreflang="pt-BR" href="{S.url(pt)}"/>',
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{S.url(en)}"/>',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{S.url(pt)}"/>',
                    '  </url>']
    out.append('</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    open('robots.txt', 'w', encoding='utf-8', newline='\n').write(
        f'User-agent: *\nAllow: /\n\nSitemap: {S.SITE}sitemap.xml\n')


for lang in ('pt', 'en'):
    print(build_index(lang))
    for post in POSTS:
        print(build_post(post, lang))
build_sitemap()
print('sitemap.xml, robots.txt')
