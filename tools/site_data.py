# -*- coding: utf-8 -*-
"""Содержимое сайта: одна таблица, из которой собираются все страницы.

Почему таблица, а не семь свёрстанных страниц. Сайту предстоит локализация, и
в тот день семь страниц превратятся в семьдесят. Разметка, которую правят
руками, к тому моменту разойдётся: где-то забудут canonical, где-то hreflang,
где-то новый пункт меню. Здесь разметка одна, а языков будет столько, сколько
понадобится.

Тексты не сочинены заново: короткие описания и списки возможностей взяты из
описаний в магазинах (`fastlane/metadata/android/en-US/`), где они уже выверены
и переведены на 61 язык. Это же и есть заготовка перевода сайта — переводить
придётся не с нуля.

Про ключевые слова. Они не в отдельном мета-теге: Google не читает
`<meta name="keywords">` с 2009 года. Слова, по которым эти страницы должны
находиться, стоят в заголовке, в первом абзаце и в подзаголовках — там, где
поисковик их действительно взвешивает. Поле `queries` ниже — это те запросы, под
которые написан текст; оно существует для того, чтобы при правке было видно,
что именно нельзя потерять.
"""

SITE = {
    'domain': 'https://eluna-apps.com',
    'name': 'Eluna',
    'author': 'Serhii Vakulenchyk',
    'email': 'support@eluna-apps.com',
    # Год для подвала. Правится раз в год и в одном месте.
    'year': 2026,
}

# `store_ids` — то, что реально опубликовано. Пустая строка значит «ещё нет», и
# страница тогда рисует не ссылку, а честную пометку: ссылка в никуда читается
# как заброшенное приложение, а не как будущее.
APPS = [
    {
        'slug': 'cycle',
        'seo_title': 'Eluna Cycle — private period tracker, no account',
        'seo_description': 'A period and ovulation tracker that keeps your health data encrypted on your phone. No sign-up, no analytics, works offline. Free.',
        'name': 'Eluna Cycle',
        'store_name': 'Eluna Cycle: Period Tracker',
        'icon': 'eluna-cycle.png',
        'appstore': '6766957276',
        'play': 'com.eluna.cycle',
        'tagline': 'Period and ovulation tracker that keeps your health data on your phone.',
        'queries': [
            'period tracker without account',
            'offline period tracker app',
            'private cycle tracking app',
            'period tracker no data sharing',
            'ovulation calendar app offline',
        ],
        'intro': (
            'Eluna Cycle is a period tracker that never asks who you are. '
            'There is no sign-up, no server of ours behind it and no analytics '
            'SDK inside it: the cycle you log, the symptoms you note and the '
            'predictions the app makes all live in an encrypted database on '
            'your own phone. Health data is the most sensitive category most '
            'people carry, and the safest place to keep it is the place it '
            'never leaves.'
        ),
        'sections': [
            ('What it tracks', [
                'Period days, flow, symptoms, mood and notes, in a calendar you can scroll back through',
                'Ovulation and fertile window, predicted on the device from your own history',
                'Cycle length, period length and their variation over time',
                'Reminders before a period is due, and for the pill, if you take one',
                'A moon calendar, if you like the ritual of it',
            ]),
            ('Why it is private', [
                'No account: nothing to register, nothing to log in to, nothing to leak',
                'The database is encrypted on the device',
                'No advertising SDK and no analytics — the app cannot report on you because it has nothing to report with',
                'Backups are yours: an encrypted file you keep, or your own cloud, never ours',
                'Every claim above is visible in the privacy policy, per feature',
            ]),
            ('Reading, not guessing', [
                'Insights explain what the app concluded and from which of your own numbers',
                'A knowledge base written in plain language, with the medical sources cited',
                'Irregular and long cycles are handled honestly, with a stated confidence rather than a false certainty',
            ]),
        ],
        'faq': [
            ('Does Eluna Cycle work offline?',
             'Yes. Everything — logging, predictions, reminders, the knowledge base — runs on the device. '
             'The app is usable with the network switched off, permanently.'),
            ('Do I need an account?',
             'No. There is no registration at all. Nothing identifies you to us, because nothing reaches us.'),
            ('Where is my health data stored?',
             'In an encrypted database on your phone. If you turn on a backup, the file is encrypted with a '
             'key we never see and stored in your own cloud.'),
            ('Is it free?',
             'Yes. No subscription, no paywall, no locked features. There is a tip jar in Settings, and it '
             'unlocks nothing.'),
        ],
    },
    {
        'slug': 'screen',
        'seo_title': 'Eluna Screen — TV show, anime & movie tracker',
        'seo_description': 'Track series, anime and films with an episode calendar and air-date reminders. Imports TV Time, Trakt and Simkl. No account, no ads, free.',
        'name': 'Eluna Screen',
        'store_name': 'Eluna Screen: TV Show Tracker',
        'icon': 'eluna-screen.png',
        'appstore': '6793637124',
        'play': 'com.eluna.screen',
        'tagline': 'TV show, anime and movie tracker with an episode calendar and no account.',
        'queries': [
            'tv show tracker app no account',
            'TV Time alternative',
            'anime tracker offline',
            'episode calendar app',
            'movie watchlist app without subscription',
        ],
        'intro': (
            'Eluna Screen knows what you are watching, which episode you stopped '
            'on and when the next one airs. That is the whole job of a TV show '
            'tracker — and this one is an anime tracker and a movie watchlist '
            'too, without ever asking who you are. No ads, no subscription, and '
            'no server of ours that could leak a watch history.'
        ),
        'sections': [
            ('Coming from another tracker', [
                'A TV Time export still works, even though the service is gone — shows, episodes and original watch dates land exactly as they were',
                'Trakt, Simkl, MyAnimeList, AniList, Kitsu, IMDb, TMDb, Letterboxd, Serializd, Bangumi, Kodi, Plex, Jellyfin and Emby import too',
                'Plex, Jellyfin and Emby also connect directly — by PIN, Quick Connect or API key',
                'Eluna never asks for another service’s password, in any scenario',
            ]),
            ('Episode tracking', [
                'TV shows, anime and films in six states, from "following" to "dropped"',
                'Mark one episode, a whole season, or everything before it',
                'Anime with absolute numbering — episode 1087 stays 1087',
                'Rewatch freely: the count goes up, your first watch date never moves',
                'How much of a season is left, counted in hours',
                'Search finds titles in any language, and descriptions are translated into yours',
            ]),
            ('Calendar and reminders', [
                'An episode calendar of what is coming, as an agenda or a month grid',
                'Reminders for a new episode, a season premiere, a finale, or a date that moved',
                'Daily and weekly digests, if one notification at a time is too many',
                'Quiet hours on by default, so nothing wakes you at four in the morning',
                'Home-screen widgets in three sizes, and an episode can be ticked off from one',
            ]),
        ],
        'faq': [
            ('Is Eluna Screen a good TV Time alternative?',
             'It imports TV Time exports with their original watch dates, which is the part most replacements '
             'lose. It also has no account, so nothing about your watch history reaches anyone.'),
            ('Does it track anime as well as TV shows?',
             'Yes, including absolute episode numbering and the current season chart. Films have their own '
             'list and their own row on the home screen.'),
            ('Does it work without an internet connection?',
             'Your library, progress and reminders are local and work offline. Fetching new air dates and '
             'searching the catalogue need the network, as they must.'),
            ('Is there a subscription?',
             'No. The app is free, without a paywall. Optional tips in Settings unlock nothing.'),
        ],
    },
    {
        'slug': 'budget',
        'seo_title': 'Eluna Budget — expense tracker, no bank login',
        'seo_description': 'An expense tracker and budget planner with no bank connection and no account. Receipts scanned on the device, database encrypted. Free.',
        'name': 'Eluna Budget',
        'store_name': 'Eluna Budget: Expense Tracker',
        'icon': 'eluna-budget.png',
        'appstore': '6799674143',
        'play': '',
        'tagline': 'Expense tracker and budget planner with no bank login and no account.',
        'queries': [
            'expense tracker without bank connection',
            'offline budget app no account',
            'envelope budgeting app private',
            'receipt scanner expense tracker offline',
            'money manager app no subscription',
        ],
        'intro': (
            'Eluna Budget is an expense tracker for people who want the numbers '
            'without handing over a bank login. There is no account to create, '
            'no server behind it and no connection to any bank. Everything is '
            'on the device, in a database encrypted with SQLCipher, and it all '
            'works with the network switched off.'
        ),
        'sections': [
            ('What you track', [
                'Expenses and income in two taps, or by photographing the receipt — the total is read on the device',
                'Budgets per category, or envelopes if you would rather give every incoming note a job',
                'Multiple accounts and currencies, with rates you can fix yourself',
                'Recurring payments, so the rent does not need retyping',
                'Statement import from a file, when the bank gives you one',
            ]),
            ('What it tells you', [
                'Where the money actually went, by category and by month',
                'Whether a budget will hold until the end of the month, at today’s pace',
                'Reports you can export as PDF or CSV and keep',
            ]),
            ('Why there is no bank login', [
                'A bank connection is a permanent credential in somebody else’s hands — this app never asks for one',
                'No account, no analytics, no advertising SDK',
                'The database is encrypted with SQLCipher on the device',
                'Backups are an encrypted file you own, or your own cloud',
            ]),
        ],
        'faq': [
            ('Does it connect to my bank?',
             'No, and that is deliberate. You add transactions yourself, photograph a receipt, or import a '
             'statement file. No credentials of yours are ever held anywhere.'),
            ('Can I use several currencies?',
             'Yes, with rates you control, and accounts in different currencies side by side.'),
            ('Is my data encrypted?',
             'The database is encrypted with SQLCipher on the device, and backups are encrypted with a key '
             'that never leaves your phone.'),
            ('Is it free?',
             'Yes, with no paywall and no subscription.'),
        ],
    },
    {
        'slug': 'reader',
        'seo_title': 'Eluna Reader — offline EPUB, PDF & comics reader',
        'seo_description': 'Read EPUB, FB2, MOBI, PDF, DjVu and comics in one offline library, with notes, highlights and text-to-speech. No subscription.',
        'name': 'Eluna Reader',
        'store_name': 'Eluna Reader: Books, EPUB PDF',
        'icon': 'eluna-reader.png',
        'appstore': '6796627281',
        'play': '',
        'tagline': 'Offline ebook reader for EPUB, PDF, FB2, MOBI, DjVu and comics.',
        'queries': [
            'offline ebook reader app',
            'epub reader without subscription',
            'fb2 mobi djvu reader ios',
            'comic book reader cbz cbr app',
            'ebook reader with notes and highlights offline',
        ],
        'intro': (
            'Eluna Reader opens almost any book you own — EPUB, FB2, MOBI, PDF, '
            'DjVu, DOC and comics, over twenty formats in one library. '
            'Everything works on the device: no account to create, no '
            'subscription, no paywall. Your books stay on your phone unless you '
            'switch on a backup yourself.'
        ),
        'sections': [
            ('Formats it reads', [
                'Books: EPUB, FB2, FB3, MOBI, AZW, AZW3, PRC',
                'Documents: PDF, DjVu, DOC, DOCX, RTF, TXT, HTML, Markdown',
                'Comics: CBZ, CBR, CB7, CBT, and folders of images',
                'Archives are opened in place, without unpacking them first',
            ]),
            ('Reading', [
                'Highlights and notes you can export',
                'Dictionaries and translation on a long press',
                'Text-to-speech, with the position kept when you switch back to reading',
                'Themes, margins, hyphenation and per-book settings',
                'Private books behind biometrics',
            ]),
            ('Your library', [
                'Organised like a file manager, not like a shop',
                'Collections, tags and search across the whole shelf',
                'OPDS catalogues, if you use them',
                'Reading progress and statistics, kept locally',
            ]),
        ],
        'faq': [
            ('Which formats does Eluna Reader support?',
             'Over twenty, including EPUB, FB2, MOBI, AZW3, PDF, DjVu, DOC, DOCX, TXT and the common comic '
             'archives CBZ, CBR, CB7 and CBT.'),
            ('Does it need an account or a subscription?',
             'Neither. The app is free, and there is nothing to register.'),
            ('Can it read books aloud?',
             'Yes, with text-to-speech that keeps your place when you go back to reading.'),
            ('Are my books uploaded anywhere?',
             'No. They stay on the device unless you turn on a backup or a sync yourself.'),
        ],
    },
    {
        'slug': 'media',
        'seo_title': 'Eluna Media — offline video, audio & photo converter',
        'seo_description': 'Convert and compress video, audio and photos on your phone. Nothing is uploaded, no watermark, no account. Hit an exact file size.',
        'name': 'Eluna Media',
        'store_name': 'Eluna Media: Video Converter',
        'icon': 'eluna-media.png',
        'appstore': '6801963204',
        'play': '',
        'tagline': 'Video, audio and photo converter that runs entirely on your phone.',
        'queries': [
            'offline video converter app',
            'video compressor without upload',
            'convert video to mp3 on phone offline',
            'photo converter heic to jpg app',
            'video converter no watermark free',
        ],
        'intro': (
            'Eluna Media converts and compresses video, photos and audio '
            'directly on your phone. Nothing is uploaded, there is no account '
            'to create and there is no server queue to wait in — every '
            'conversion runs locally through a bundled FFmpeg engine, so your '
            'files never leave the device.'
        ),
        'sections': [
            ('What it converts', [
                'Video: MP4, MOV, MKV, AVI, WebM and more, with codec and bitrate under your control',
                'Audio: MP3, AAC, FLAC, WAV, OGG — including pulling the sound out of a video',
                'Photos: HEIC, JPEG, PNG, WebP, AVIF, with batch conversion',
                'GIFs, from a clip or from a burst of photos',
            ]),
            ('What it does besides converting', [
                'Compress to an exact file size — useful when a form refuses anything above a limit',
                'Trim, crop, rotate and merge clips',
                'Hundreds of files in one queue, processed while you do something else',
            ]),
            ('You do not have to take privacy on trust', [
                'The release build ships without the INTERNET permission on Android',
                'Your phone’s own app info screen will confirm the app has no network access at all',
                'No account, no analytics, no watermark on the result',
            ]),
        ],
        'faq': [
            ('Are my files uploaded to a server?',
             'No. Conversion runs on the device through a bundled FFmpeg engine. On Android the release '
             'build has no INTERNET permission at all, which your phone will confirm.'),
            ('Does it add a watermark?',
             'No. The output is the file you converted, nothing added.'),
            ('Can it hit an exact file size?',
             'Yes — you set the target size and the app works out the bitrate.'),
            ('Is it free?',
             'Yes, with no subscription and no export limit.'),
        ],
    },
    {
        'slug': 'subs',
        'seo_title': 'Eluna Subs — subscription tracker and renewal alerts',
        'seo_description': 'See every subscription, what it costs per month, and get a reminder before it renews or a free trial ends. No bank access, no account.',
        'name': 'Eluna Subs',
        'store_name': 'Eluna Subs: Subscription Tracker',
        'icon': 'eluna-subs.png',
        'appstore': '6802049185',
        'play': '',
        'tagline': 'Subscription tracker that reminds you before the money leaves.',
        'queries': [
            'subscription tracker app no bank access',
            'free trial reminder app',
            'subscription manager offline',
            'app to track recurring payments privately',
            'cancel subscription reminder app',
        ],
        'intro': (
            'Eluna Subs remembers what renews and when, and tells you before '
            'the money leaves — not after. It never connects to a bank, it '
            'never asks you to register, and it works with the network switched '
            'off.'
        ),
        'sections': [
            ('Reminders that arrive in time', [
                'Before a renewal, with as many days of warning as you want',
                'Before a free trial ends — the one deadline that actually costs money to miss',
                'Reminders survive a reboot and land on the minute your phone allows',
            ]),
            ('The real cost', [
                'What every subscription costs per month and per year, whatever period it is billed in',
                'The total, so the sum is a number and not a feeling',
                'Several currencies, with rates you control',
            ]),
            ('Kept to yourself', [
                'No bank connection and no card details — you enter what you pay',
                'No account and no analytics',
                'The database is encrypted on the device; backups are yours',
            ]),
        ],
        'faq': [
            ('Does it need access to my bank or cards?',
             'No. You enter the subscriptions yourself. The app has no bank connection of any kind.'),
            ('Will it remind me before a free trial ends?',
             'Yes, and that is the reminder it was built around.'),
            ('Does it work offline?',
             'Yes, entirely.'),
            ('Is it free?',
             'Yes, with no subscription of its own — which would be a strange thing for this app to have.'),
        ],
    },
    {
        'slug': 'kitchen',
        'seo_title': 'Eluna Kitchen — recipes with computed nutrition',
        'seo_description': 'A recipe book and food diary where calories are computed from weighed ingredients and USDA data, not guessed. No account, no subscription.',
        'name': 'Eluna Kitchen',
        'store_name': 'Eluna Kitchen: Calorie Counter',
        'icon': 'eluna-kitchen.png',
        'appstore': '',
        'play': '',
        'tagline': 'Recipe book and food diary where the calories are computed, not guessed.',
        'queries': [
            'calorie counter without subscription',
            'recipe app with nutrition calculation',
            'food diary offline app',
            'calorie counter no account',
        ],
        'intro': (
            'Eluna Kitchen is a recipe book and a food diary in one. Every '
            'ingredient is weighed and matched to USDA data, so the calories '
            'and macros are computed from what you actually cooked rather than '
            'guessed from a photograph.'
        ),
        'sections': [
            ('Recipes and the diary', [
                'Your own recipes, with per-portion nutrition worked out from the ingredients',
                'A food diary that adds up the day without a subscription prompt',
                'Ingredients matched to USDA data rather than to a crowd-sourced guess',
            ]),
            ('The Eluna rules, as usual', [
                'No account, no analytics, no advertising SDK',
                'The database is on your device',
                'Free, with an optional tip that unlocks nothing',
            ]),
        ],
        'faq': [
            ('Is Eluna Kitchen available yet?',
             'Not yet. It is in review for the App Store; this page will carry the link the day it ships.'),
            ('Will it require a subscription?',
             'No. Like every Eluna app, it is free, with an optional tip that unlocks nothing.'),
        ],
    },
]

# Общие обещания семьи — они же то, ради чего человек ищет «no account» и
# «offline». Стоят и на главной, и внизу каждой страницы приложения.
PROMISES = [
    'No sign-up, ever',
    'No subscriptions, no paywalls',
    'No analytics or crash SDKs',
    'No ads',
    'Tips, if you feel like it; they unlock nothing',
    'Encrypted, user-owned backups',
]


def app_by_slug(slug):
    for app in APPS:
        if app['slug'] == slug:
            return app
    raise KeyError(slug)
