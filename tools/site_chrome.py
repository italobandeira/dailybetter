"""Shared chrome (head links, header, footer) for the static pages, per language."""
import re

SITE = 'https://italobandeira.github.io/dailybetter/'
PLAY = 'https://play.google.com/store/apps/details?id=com.iflag.dailybetter_mood_tracker'

T = {
    'pt': {
        'html_lang': 'pt-BR', 'og_locale': 'pt_BR', 'og_alt': 'en_US',
        'skip': 'Pular para o conteúdo', 'home_aria': 'DailyBetter, página inicial',
        'nav_aria': 'Navegação', 'privacy': 'Privacidade', 'terms': 'Termos', 'blog': 'Blog', 'contact': 'Contato',
        'back': 'Voltar ao site', 'other_code': 'EN', 'other_aria': 'English version', 'other_name': 'English',
        'other_hreflang': 'en',
        'tagline': 'Diário de humor grátis para Android. Um espaço para todos os seus dias.',
        'store': 'Baixar no Google Play', 'product': 'Produto', 'how': 'Como funciona', 'features': 'Recursos',
        'screens': 'Telas', 'support': 'Suporte', 'faq': 'Perguntas frequentes', 'email': 'E-mail',
        'legal': 'Legal', 'privacy_long': 'Privacidade', 'terms_long': 'Termos de Uso',
        'rights': '© 2026 DailyBetter. Todos os direitos reservados.', 'made': 'Desenvolvido por iFlag',
    },
    'en': {
        'html_lang': 'en', 'og_locale': 'en_US', 'og_alt': 'pt_BR',
        'skip': 'Skip to content', 'home_aria': 'DailyBetter, home page',
        'nav_aria': 'Navigation', 'privacy': 'Privacy', 'terms': 'Terms', 'blog': 'Blog', 'contact': 'Contact',
        'back': 'Back to site', 'other_code': 'PT', 'other_aria': 'Versão em português', 'other_name': 'Português',
        'other_hreflang': 'pt-BR',
        'tagline': 'A free mood tracker for Android. A space for all your days.',
        'store': 'Get it on Google Play', 'product': 'Product', 'how': 'How it works', 'features': 'Features',
        'screens': 'Screens', 'support': 'Support', 'faq': 'FAQ', 'email': 'Email',
        'legal': 'Legal', 'privacy_long': 'Privacy', 'terms_long': 'Terms of Use',
        'rights': '© 2026 DailyBetter. All rights reserved.', 'made': 'Made by iFlag',
    },
}


def lang_of(path):
    return 'en' if path.startswith('en/') else 'pt'


def root_rel(path):
    """Relative prefix from the page to the site root (where assets live)."""
    return '../' * path.count('/')


def home_rel(path):
    """Relative prefix from the page to its language home."""
    inner = path[3:] if path.startswith('en/') else path
    return '../' * inner.count('/')


def url(path):
    return SITE + (path[:-len('index.html')] if path.endswith('index.html') else path)


def head_links(path, alt_path):
    pt, en = (path, alt_path) if lang_of(path) == 'pt' else (alt_path, path)
    return (f'  <link rel="canonical" href="{url(path)}">\n'
            f'  <link rel="alternate" hreflang="pt-BR" href="{url(pt)}">\n'
            f'  <link rel="alternate" hreflang="en" href="{url(en)}">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{url(pt)}">\n')


def header(path, alt_path, current):
    t = T[lang_of(path)]
    h = home_rel(path)
    r = root_rel(path)

    def item(key, href):
        cur = ' aria-current="page"' if key == current else ''
        return f'        <a href="{h}{href}"{cur}>{t[key]}</a>\n'

    return (
        '  <header class="site-header">\n'
        '    <div class="wrap header-inner">\n'
        f'      <a class="brand-logo" href="{h}index.html" aria-label="{t["home_aria"]}">\n'
        f'        <img src="{r}assets/moods/excellent.png" alt="" width="36" height="36">\n'
        '        <span>Daily<em>Better</em></span>\n'
        '      </a>\n'
        f'      <nav class="header-nav" aria-label="{t["nav_aria"]}">\n'
        + item('blog', 'blog/index.html')
        + item('privacy', 'privacy.html')
        + item('terms', 'terms.html')
        + item('contact', 'contact.html')
        + f'        <a class="lang-link" href="{r}{alt_path}" hreflang="{t["other_hreflang"]}" lang="{t["other_hreflang"]}" aria-label="{t["other_aria"]}">{t["other_code"]}</a>\n'
        f'        <a class="home-link" href="{h}index.html">{t["back"]}</a>\n'
        '      </nav>\n'
        '    </div>\n'
        '  </header>'
    )


def footer(path, alt_path, current):
    t = T[lang_of(path)]
    h = home_rel(path)
    r = root_rel(path)

    def li(label, href, key=None):
        cur = ' aria-current="page"' if key and key == current else ''
        return f'              <li><a href="{href}"{cur}>{label}</a></li>\n'

    return (
        '  <footer class="site-footer">\n'
        '    <div class="footer-inner">\n'
        '      <div class="footer-top">\n'
        '        <div class="footer-brand">\n'
        f'          <a class="brand-logo" href="{h}index.html" aria-label="{t["home_aria"]}"><img src="{r}assets/moods/excellent.png" alt="" width="36" height="36"><span>Daily<em>Better</em></span></a>\n'
        f'          <p class="footer-tagline">{t["tagline"]}</p>\n'
        f'          <a class="footer-store" href="{PLAY}" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 3 15 9-15 9V3Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="m5 3 10 12m-10 6 10-12" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>{t["store"]}</a>\n'
        '        </div>\n'
        '        <div class="footer-columns">\n'
        '          <nav class="footer-column" aria-labelledby="footer-produto">\n'
        f'            <h2 id="footer-produto">{t["product"]}</h2>\n'
        '            <ul>\n'
        + li(t['how'], f'{h}index.html#como-funciona')
        + li(t['features'], f'{h}index.html#recursos')
        + li(t['screens'], f'{h}index.html#telas')
        + li(t['blog'], f'{h}blog/index.html', 'blog')
        + '            </ul>\n'
        '          </nav>\n'
        '          <nav class="footer-column" aria-labelledby="footer-suporte">\n'
        f'            <h2 id="footer-suporte">{t["support"]}</h2>\n'
        '            <ul>\n'
        + li(t['faq'], f'{h}index.html#duvidas')
        + li(t['contact'], f'{h}contact.html', 'contact')
        + li(t['email'], 'mailto:iflagdev@gmail.com')
        + '            </ul>\n'
        '          </nav>\n'
        '          <nav class="footer-column" aria-labelledby="footer-legal">\n'
        f'            <h2 id="footer-legal">{t["legal"]}</h2>\n'
        '            <ul>\n'
        + li(t['privacy_long'], f'{h}privacy.html', 'privacy')
        + li(t['terms_long'], f'{h}terms.html', 'terms')
        + '            </ul>\n'
        '          </nav>\n'
        '        </div>\n'
        '      </div>\n'
        '      <div class="footer-bottom">\n'
        f'        <p>{t["rights"]}</p>\n'
        f'        <p><a href="{r}{alt_path}" hreflang="{t["other_hreflang"]}" lang="{t["other_hreflang"]}">{t["other_name"]}</a> · {t["made"]}</p>\n'
        '      </div>\n'
        '    </div>\n'
        '  </footer>'
    )


def apply_chrome(html, path, alt_path, current):
    """Swap header/footer for the shared ones and add canonical + hreflang links."""
    html = re.sub(r'  <header class="site-header">.*?</header>', lambda m: header(path, alt_path, current), html, count=1, flags=re.S)
    html = re.sub(r'  <footer class="site-footer">.*?</footer>', lambda m: footer(path, alt_path, current), html, count=1, flags=re.S)
    html = re.sub(r'  <link rel="(canonical|alternate)"[^>]*>\n', '', html)
    html = html.replace('  <meta name="robots" content="index, follow">\n',
                        '  <meta name="robots" content="index, follow">\n' + head_links(path, alt_path), 1)
    return html
