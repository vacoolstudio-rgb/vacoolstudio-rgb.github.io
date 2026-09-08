# -*- coding: utf-8 -*-
"""Сообщает поисковикам, что страницы изменились.

    python3 tools/ping_indexnow.py            # все адреса из sitemap.xml
    python3 tools/ping_indexnow.py /screen/   # только эти

Кого это касается. Bing принимает такие уведомления, а вместе с ним их получают
DuckDuckGo, Yahoo и Ecosia — они берут индекс у Bing. Yandex принимает тоже.
**Google протокол не поддерживает**: туда адреса попадают через Search Console и
`sitemap.xml`, и это ручной шаг, который автоматизировать нечем — Indexing API
Google открыт только для вакансий и трансляций, для остальных страниц его
использование прямо запрещено правилами.

Почему это вообще работает. По адресу `/<ключ>.txt` лежит файл с тем же ключом —
так поисковик убеждается, что уведомляет владелец сайта, а не прохожий. Ключ
записан в `build_site.py`, поэтому файл переживает пересборку.

Ответ 202 значит «принято к обработке», а не «проиндексировано». Индексация —
решение поисковика, и на молодом домене она занимает дни или недели; уведомление
лишь снимает ожидание обхода.
"""

import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_site import INDEXNOW_KEY  # noqa: E402
from site_data import SITE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = SITE['domain'].replace('https://', '').replace('http://', '')

ENDPOINTS = (
    'https://api.indexnow.org/indexnow',   # Bing, а с ним DuckDuckGo, Yahoo, Ecosia
    'https://yandex.com/indexnow',
)


def urls_from_sitemap():
    with io.open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8') as f:
        return re.findall(r'<loc>(.*?)</loc>', f.read())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    urls = ([SITE['domain'] + a if a.startswith('/') else a for a in args]
            if args else urls_from_sitemap())
    if not urls:
        raise SystemExit('нечего отправлять')

    payload = json.dumps({
        'host': HOST,
        'key': INDEXNOW_KEY,
        'keyLocation': '%s/%s.txt' % (SITE['domain'], INDEXNOW_KEY),
        'urlList': urls,
    }).encode()

    print('адресов: %d' % len(urls))
    failed = False
    for endpoint in ENDPOINTS:
        request = urllib.request.Request(
            endpoint, data=payload,
            headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                print('%-34s HTTP %s' % (endpoint, response.status))
        except urllib.error.HTTPError as e:
            # 422 обычно значит, что ключа нет по указанному адресу — то есть
            # сборка выложена не полностью.
            body = ''
            try:
                body = e.read().decode()[:200]
            except Exception:
                pass
            print('%-34s HTTP %s %s' % (endpoint, e.code, body))
            failed = True
        except Exception as e:
            print('%-34s не удалось: %s' % (endpoint, e))
            failed = True

    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
