# -*- coding: utf-8 -*-
"""Собирает сайт из `site_data.py`.

    python3 tools/build_site.py            # записать
    python3 tools/build_site.py --check    # проверить, что записанное совпадает

Что получается:

    /                 главная со списком приложений
    /<app>/           страница приложения (cycle, screen, budget, reader, …)
    /sitemap.xml      карта сайта
    /robots.txt

Почему генератор. Сайту предстоит локализация, и тогда семь страниц станут
семьюдесятью. Разметка, которую правят руками, к тому моменту разойдётся: где-то
забудут canonical, где-то hreflang, где-то новый пункт меню. Здесь разметка одна.

Про индексацию — то, что делает эта сборка и что должен знать следующий:

* **Отдельный адрес на приложение.** Одна страница со списком из семи не может
  ранжироваться ни по одному конкретному запросу: у неё один `<title>`, одно
  описание и текст, размазанный между «трекером цикла» и «конвертером видео».
  Семь страниц — семь заголовков, каждый под свой запрос.
* **Разметка Schema.org** (`SoftwareApplication`, `FAQPage`, `BreadcrumbList`).
  Первое даёт карточку приложения в выдаче, второе — раскрывающиеся вопросы,
  третье — «хлебные крошки» вместо голого адреса.
* **`<meta name="keywords">` не выводится намеренно.** Google не читает его с
  2009 года, а перечисление ключевых слов в коде страницы — сигнал спама. Слова
  стоят там, где их взвешивают: в заголовке, первом абзаце и подзаголовках.
* **`hreflang` уже выводится**, пока с одним языком и `x-default`. Когда
  появятся переводы, добавится язык в `LOCALES` — и ссылки проставятся сами.
"""

import html
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from site_data import (APPS, PROMISES, SITE, is_released,  # noqa: E402
                       released_apps, upcoming_apps)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Языки сайта. Пока один; когда появятся переводы, они встанут в `/<lang>/…`,
# а `hreflang` проставится сам. Первый в списке — язык корня.
LOCALES = ['en']

E = html.escape


def path_for(app_slug=None, locale='en'):
    """Адрес страницы. Корень — язык по умолчанию, остальные под своим префиксом."""
    prefix = '' if locale == LOCALES[0] else '/' + locale
    return (prefix + '/' + app_slug + '/') if app_slug else (prefix + '/')


def head(title, description, canonical, *, app_slug=None, extra=''):
    """Шапка страницы: то, что читают поисковик и превью в мессенджере."""
    url = SITE['domain'] + canonical
    alternates = '\n'.join(
        '<link rel="alternate" hreflang="%s" href="%s">'
        % (loc, SITE['domain'] + path_for(app_slug, loc)) for loc in LOCALES
    )
    return f'''<!DOCTYPE html>
<html lang="{LOCALES[0]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{E(url)}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{E(SITE['domain'] + path_for(app_slug, LOCALES[0]))}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(SITE['name'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{E(url)}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{'/styles.css'}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌙</text></svg>">
{extra}</head>
<body>
<div class="ambient"></div>
<div class="wrap">

<header class="site">
  <a class="brand" href="/">Eluna<span>.</span></a>
  <nav class="site">
    <a href="/#apps">Apps</a>
    <a href="/privacy/">Privacy &amp; Terms</a>
    <a href="mailto:{E(SITE['email'])}">Support</a>
  </nav>
</header>
'''


def foot():
    return f'''
<footer class="site">
  <span>© {SITE['year']} {E(SITE['name'])} · {E(SITE['author'])}</span>
  <span><a href="/privacy/">Privacy &amp; Terms</a> · <a href="mailto:{E(SITE['email'])}">{E(SITE['email'])}</a></span>
  <span class="fine">Set in <a href="https://github.com/sharanda/manrope">Manrope</a>
  by Mikhail Sharanda, used under the
  <a href="https://openfontlicense.org/">SIL Open Font License 1.1</a>.</span>
</footer>

</div>
</body>
</html>
'''


def store_links(app, *, big=False):
    """Ссылки в магазины — только на то, что действительно опубликовано."""
    cls = 'btn primary' if big else ''
    out = []
    if app['appstore']:
        out.append('<a class="%s" href="https://apps.apple.com/app/id%s">App Store</a>'
                   % (cls, app['appstore']))
    else:
        out.append('<span class="badge">Soon on the App Store</span>')
    if app['play']:
        out.append('<a class="%s" href="https://play.google.com/store/apps/details?id=%s">Google Play</a>'
                   % ('btn ghost' if big else '', app['play']))
    else:
        out.append('<span class="badge">Soon on Google Play</span>')
    return '\n        '.join(out)


def json_ld(app):
    """Разметка для поисковика: карточка приложения и блок вопросов.

    Ни рейтинга, ни числа отзывов здесь нет намеренно. Google требует, чтобы
    такие поля отражали то, что видно на странице; выдуманный рейтинг — повод
    снять разметку целиком, а не украшение выдачи.
    """
    url = SITE['domain'] + path_for(app['slug'])
    systems = []
    if app['appstore']:
        systems.append('iOS')
    if app['play']:
        systems.append('Android')
    os_line = ', '.join(systems) or 'iOS, Android'

    faq = ',\n      '.join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (js(q), js(a)) for q, a in app['faq']
    )

    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "SoftwareApplication",
      "name": {js(app['store_name'])},
      "applicationCategory": "MobileApplication",
      "operatingSystem": {js(os_line)},
      "url": {js(url)},
      "description": {js(app['tagline'])},
      "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
      "author": {{"@type": "Person", "name": {js(SITE['author'])}}}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"Eluna","item":{js(SITE['domain'] + '/')}}},
        {{"@type":"ListItem","position":2,"name":{js(app['name'])},"item":{js(url)}}}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
      {faq}
      ]
    }}
  ]
}}
</script>
'''


def js(value):
    """Строка внутри JSON-LD."""
    return '"%s"' % (value.replace('\\', '\\\\').replace('"', '\\"')
                     .replace('\n', ' '))


def app_page(app):
    # Заголовок и описание заданы в данных, а не собраны из tagline: Google
    # обрезает title примерно на 60 знаках, а description на 155, и обрезанное
    # предложение читается в выдаче как сломанное. Длину стережёт `check_seo`.
    title = app['seo_title']
    description = app['seo_description']

    sections = []
    for heading, items in app['sections']:
        bullets = '\n'.join('    <li>%s</li>' % E(i) for i in items)
        sections.append('  <h2>%s</h2>\n  <ul class="feature-list">\n%s\n  </ul>'
                        % (E(heading), bullets))

    faq = '\n'.join(
        '  <details class="faq">\n    <summary>%s</summary>\n    <p>%s</p>\n  </details>'
        % (E(q), E(a)) for q, a in app['faq']
    )

    promises = '\n'.join('    <li>%s</li>' % E(p) for p in PROMISES)

    others = '\n'.join(
        '      <li><a href="%s">%s</a> <span class="kind">%s</span></li>'
        % (path_for(o['slug']), E(o['name']), E(o['tagline']))
        for o in released_apps() if o['slug'] != app['slug']
    )

    return (
        head(title, description, path_for(app['slug']),
             app_slug=app['slug'], extra=json_ld(app))
        + f'''
<main>
  <nav class="crumbs" aria-label="Breadcrumb">
    <a href="/">Eluna</a> › <span>{E(app['name'])}</span>
  </nav>

  <section class="hero app-hero">
    <img class="icon big" src="/icons/{app['icon']}" width="192" height="192"
         alt="{E(app['name'])} app icon" decoding="async">
    <div>
      <h1>{E(app['name'])}</h1>
      <p class="tagline">{E(app['tagline'])}</p>
      <div class="cta">
        {store_links(app, big=True)}
      </div>
    </div>
  </section>

  <p class="lede">{E(app['intro'])}</p>

{chr(10).join(sections)}

  <h2>Questions</h2>
{faq}

  <h2>The rules every Eluna app follows</h2>
  <ul class="pillars">
{promises}
  </ul>
  <p>What each app does and does not send anywhere is written out, per app, in the
  <a href="/privacy/">privacy policy and terms of use</a>.</p>

  <h2>The other Eluna apps</h2>
  <ul class="other-apps">
{others}
  </ul>
</main>
'''
        + foot()
    )


def index_page():
    title = 'Eluna — local-first apps with no account and no ads'
    # 160 знаков — предел, после которого Google обрезает описание в выдаче.
    description = ('Local-first iPhone and Android apps: period tracker, TV show tracker, '
                   'expense tracker, ebook reader, converter. No accounts, no analytics.')

    cards = []
    for app in released_apps():
        cards.append(f'''    <li class="app-card">
      <a class="card-link" href="{path_for(app['slug'])}">
        <img class="icon" src="/icons/{app['icon']}" width="192" height="192"
             alt="" loading="lazy" decoding="async">
        <h3>{E(app['name'])}</h3>
        <p class="kind">{E(app['tagline'])}</p>
      </a>
      <div class="links">
        {store_links(app)}
      </div>
    </li>''')

    # Приложения в работе — одной строкой, без собственных адресов. Человеку
    # видно, что проект живой; поисковику не достаётся страниц, которым нечего
    # сказать.
    upcoming = upcoming_apps()
    in_progress = ''
    if upcoming:
        names = ', '.join(E(a['name']) for a in upcoming)
        in_progress = ('\n  <h2>In the works</h2>\n'
                       '  <p class="lede">%s. Each gets its own page here the day '
                       'it reaches the store.</p>\n' % names)

    promises = '\n'.join('    <li>%s</li>' % E(p) for p in PROMISES)

    ld = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Eluna",
  "url": "%s/",
  "email": "%s",
  "founder": {"@type": "Person", "name": "%s"}
}
</script>
''' % (SITE['domain'], SITE['email'], SITE['author'])

    return (
        head(title, description, path_for(), extra=ld)
        + f'''
<main>
  <section class="hero">
    <h1>Apps that keep your life <em>on your phone</em>.</h1>
    <p class="tagline">Eluna builds local-first apps for Android and iOS. No accounts,
    no servers of ours, no analytics — what you write down stays in a database on
    your own device, and we couldn’t read it if we wanted to.</p>
    <div class="cta">
      <a class="btn primary" href="#apps">See the apps</a>
      <a class="btn ghost" href="/privacy/">Read the privacy policy</a>
    </div>
  </section>

  <ul class="pillars">
{promises}
  </ul>

  <h2 id="apps">The apps</h2>
  <ul class="apps">
{chr(10).join(cards)}
  </ul>
{in_progress}

  <h2>One policy, honestly written</h2>
  <p>Every Eluna app is covered by a single
  <a href="/privacy/">privacy policy and terms of use</a> that says, per app,
  exactly what leaves your device and how to stop it. The short version: almost
  nothing does.</p>
</main>
'''
        + foot()
    )


def sitemap():
    # Только то, что существует: адрес в карте сайта, отдающий 404, — это ошибка
    # обхода в Search Console, а не отсутствующая страница.
    urls = [path_for(), '/privacy/'] + [path_for(a['slug']) for a in released_apps()]
    entries = '\n'.join(
        '  <url><loc>%s%s</loc></url>' % (SITE['domain'], u) for u in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'
            .replace('www.sitemap.org', 'www.sitemaps.org')
            + entries + '\n</urlset>\n')


# Ключ IndexNow. Bing, Yandex и Seznam принимают уведомление об изменившихся
# адресах только если по адресу  лежит файл с этим же ключом — так
# они проверяют, что уведомляет владелец сайта. Google протокол не поддерживает:
# туда адреса попадают через Search Console и sitemap.
INDEXNOW_KEY = '04ca432d89444214907e84081c0d30a3'


def robots():
    return ('User-agent: *\n'
            'Allow: /\n\n'
            'Sitemap: %s/sitemap.xml\n' % SITE['domain'])


def write(path, body, check, changed):
    full = os.path.join(ROOT, path.lstrip('/'))
    if os.path.exists(full):
        with io.open(full, encoding='utf-8') as f:
            if f.read() == body:
                return
    changed.append(path)
    if check:
        return
    directory = os.path.dirname(full)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    with io.open(full, 'w', encoding='utf-8', newline='\n') as f:
        f.write(body)


def check_seo():
    """Длины, на которых поисковик режет строку, и уникальность заголовков.

    Два приложения с одинаковым `title` соревнуются друг с другом за один и тот
    же запрос, и выигрывает случайное.
    """
    seen = {}
    problems = []
    for app in released_apps():
        title, desc = app['seo_title'], app['seo_description']
        if len(title) > 60:
            problems.append('%s: title %d знаков (>60)' % (app['slug'], len(title)))
        if len(desc) > 160:
            problems.append('%s: description %d знаков (>160)' % (app['slug'], len(desc)))
        if len(desc) < 70:
            problems.append('%s: description %d знаков — слишком коротко' % (app['slug'], len(desc)))
        for field, value in (('title', title), ('description', desc)):
            key = (field, value)
            if key in seen:
                problems.append('%s и %s делят один %s' % (app['slug'], seen[key], field))
            seen[key] = app['slug']
    if problems:
        raise SystemExit('SEO: ' + '; '.join(problems))


def main():
    check = '--check' in sys.argv[1:]
    check_seo()
    changed = []

    write('index.html', index_page(), check, changed)
    for app in released_apps():
        write('%s/index.html' % app['slug'], app_page(app), check, changed)
    write('sitemap.xml', sitemap(), check, changed)
    write('robots.txt', robots(), check, changed)
    write('%s.txt' % INDEXNOW_KEY, INDEXNOW_KEY + chr(10), check, changed)

    if check:
        if changed:
            raise SystemExit('расходятся с данными (%d): %s\nзапустите '
                             'tools/build_site.py' % (len(changed), ' '.join(changed)))
        print('%d страниц приложений + главная: собрано' % len(released_apps()))
    else:
        print('%d страниц приложений (+%d в работе), записано файлов: %d'
              % (len(released_apps()), len(upcoming_apps()), len(changed)))


if __name__ == '__main__':
    main()
