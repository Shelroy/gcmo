"""Builds the GCMC static site into ./site.

Run:  python3 build.py
Pages are generated from the templates below, so edit this file (not the HTML in site/)
and re-run it. Images live in site/assets/img/work and are described in manifest.json.
"""
import base64, hashlib, html, io, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'site') + '/'
SITE = 'https://gcmcgeo.com'
PHONE = '+592 609 7398'
TEL = '+5926097398'
EMAIL = 'jleegcmc@gmail.com'
# Cloudflare Turnstile site key (public). This is Cloudflare's always-pass TEST key:
# replace it with the real site key from Cloudflare → Turnstile before going live.
TURNSTILE_SITE_KEY = '1x00000000000000000000AA'
LASTMOD = '2026-10-31'

MAN = {m['slug']: m for m in json.load(open(ROOT + 'assets/img/manifest.json'))}
esc = html.escape

def file_hash(path):
    return hashlib.md5(open(ROOT + path, 'rb').read()).hexdigest()[:8]
CSS_V, JS_V = file_hash('assets/css/style.css'), file_hash('assets/js/main.js')

# Tiny blurred placeholders, shown behind each photo while it loads
LQIP = {}
for slug in MAN:
    im = Image.open(f'{ROOT}assets/img/work/{slug}-800.webp').convert('RGB')
    im.thumbnail((24, 24))
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=40)
    LQIP[slug] = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()

CATS = {
    'commercial': 'Commercial & entertainment',
    'construction': 'Construction in progress',
    'residential': 'Residential interiors',
    'mep': 'Mechanical & electrical',
}
CASES = {
    'cinema-fit-out': dict(
        title='Cinema & entertainment fit-out', nav='Cinema fit-out', cats=('commercial', 'construction', 'mep'),
        hero='cinema-lobby-purple-lighting', card='cinema-auditorium-screen',
        summary='A large commercial interior taken from open steel shell to finished cinema: lobby, concession stands, auditoriums and the plant rooms behind them.'),
    'residential-renovations': dict(
        title='Residential renovations', nav='Residential renovations', cats=('residential',),
        hero='open-plan-kitchen', card='living-room-renovation',
        summary='Kitchens, bathrooms and living spaces renovated to update the layout, the look and the way a home works.'),
}
def case_for(cat):
    return next(k for k, c in CASES.items() if cat in c['cats'])

def title_of(slug):
    return slug.replace('-', ' ').capitalize().replace('Ups ', 'UPS ').replace('Upper level', 'Upper-level')

def img(slug, sizes='100vw', cls='', lazy=True, parallax=None, alt=None):
    m = MAN[slug]
    srcset = f'/assets/img/work/{slug}-800.webp 800w, /assets/img/work/{slug}-1600.webp 1600w'
    if slug == 'cinema-lobby-blue-lighting':
        srcset += f', /assets/img/work/{slug}-2400.webp 2400w'
    a = esc(alt if alt is not None else m['alt'])
    extra = f' class="{cls}"' if cls else ''
    px = f' data-parallax="{parallax}"' if parallax else ''
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    return (f'<img src="/assets/img/work/{slug}-1600.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{m["w"]}" height="{m["h"]}" alt="{a}"{extra}{px}{load} '
            f'style="background-image:url({LQIP[slug]})">')

ARROW = '<svg class="btn__arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_S = ARROW.replace('class="btn__arrow" ', '')
ARROW_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'

def icon(paths, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'

ICONS = {
    'construction': '<path d="M6 42h36M10 42V22h14v20M24 42V14h14v28"/><path d="M14 27h6M14 33h6M28 19h6M28 25h6M28 31h6M28 37h6"/><path d="M4 10l20-6 20 6"/><path d="M24 4v10"/>',
    'management': '<rect x="11" y="8" width="26" height="34" rx="2"/><path d="M18 8V5h12v3"/><path d="M17 20l3 3 6-6M17 32h14M17 37h9"/>',
    'renovation': '<path d="M6 22L24 7l18 15"/><path d="M11 18v24h26V18"/><path d="M20 42V31h8v11"/><path d="M33 4l6 6-3 3-6-6z"/><path d="M33 13l-6 6"/>',
    'property': '<rect x="7" y="16" width="20" height="26"/><path d="M27 24h14v18H27"/><path d="M12 22h4M12 28h4M12 34h4M19 22h3M19 28h3M19 34h3"/><circle cx="33" cy="10" r="5"/><path d="M33 15v5"/>',
    'ac': '<rect x="5" y="8" width="38" height="14" rx="2"/><path d="M10 17h28"/><path d="M16 28v12M24 28v14M32 28v12"/><path d="M13 31l3-3 3 3M21 33l3-3 3 3M29 31l3-3 3 3"/>',
    'pool': '<path d="M14 30V8a4 4 0 018 0M30 30V8a4 4 0 018 0"/><path d="M14 16h16M14 23h16"/><path d="M4 36c4 0 4-3 8-3s4 3 8 3 4-3 8-3 4 3 8 3 4-3 8-3"/><path d="M4 43c4 0 4-3 8-3s4 3 8 3 4-3 8-3 4 3 8 3 4-3 8-3"/>',
    'retail': '<path d="M10 16h28l-2 26H12z"/><path d="M18 20v-6a6 6 0 0112 0v6"/>',
    'office': '<rect x="6" y="15" width="36" height="25" rx="2"/><path d="M18 15v-5h12v5M6 26h36M22 26v4h4v-4"/>',
    'hotel': '<path d="M5 40V12M5 32h38v8M43 32v-6a6 6 0 00-6-6H20v12"/><circle cx="12" cy="24" r="4"/>',
    'education': '<path d="M24 10L3 19l21 9 21-9z"/><path d="M11 23v10c4 4 22 4 26 0V23M45 19v12"/>',
    'institutional': '<path d="M6 18L24 7l18 11M8 42h32M10 18v20M18 18v20M30 18v20M38 18v20M6 38h36"/>',
    'new': '<path d="M8 42V6h4v36M12 8h30l-4 6H12"/><path d="M34 14v8"/><rect x="30" y="22" width="8" height="6"/><path d="M4 42h40"/>',
    'tenant': '<path d="M6 42V10h22v32M28 18h14v24"/><path d="M12 16h4M20 16h2M12 24h4M20 24h2M12 32h4M20 32h2"/><path d="M15 42v-5h4v5"/>',
    'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0114 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'pause': '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>',
    'play': '<path d="M7 5l12 7-12 7z"/>',
}
def small_icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

SERVICES = [
    dict(id='general-construction', icon='construction', name='General Construction', img='upper-level-escalator',
         short='Small to medium commercial projects, from office and restaurant refurbishments to complete small industrial units.',
         body=['Building services to the commercial sector are within our scope. We deliver small to medium-sized projects, which may include office or restaurant refurbishments, extensions to commercial premises, complete construction of small industrial units, change of use on commercial premises and hard landscaping to external areas.'],
         checks=['Office and restaurant refurbishments', 'Extensions to commercial premises', 'Small industrial units, built complete', 'Change of use on commercial premises', 'Hard landscaping to external areas']),
    dict(id='construction-management', icon='management', name='Construction Management', img='site-walkthrough',
         short='The expertise of a large firm with a boutique, top-down approach, and one team from principals to labourers on site.',
         body=['With over a decade of trusted experience, GCMC has grown to become one of the top general contracting and construction management firms in the Caribbean. The cornerstones of our business are solid construction and excellence in on-site management.',
               'We bring our clients the expertise and full capabilities of a large firm, while keeping a boutique approach with top-down involvement. At GCMC, our teams work together on every project, small and large, from principals and directors to project managers, estimators, supervisors and our labourers on site.'],
         checks=['Principals and directors involved throughout', 'Project managers, estimators and supervisors on one team', 'Excellence in on-site management', 'One contact for your whole project']),
    dict(id='building-renovation', icon='renovation', name='Building Renovation', img='living-room-renovation',
         short='Renovations that breathe new life into tired buildings, including listed and heritage properties.',
         body=['Renovation projects breathe new life into tired homes. We have significant experience working with listed buildings and buildings within heritage and conservation areas, and we use building techniques that are sympathetic to the building.',
               'You can update the layout to create better spaces, make structural changes, or simply modernise what already exists. There are endless possibilities for changing the look, function and feel of your renovation project.'],
         checks=['Listed buildings, heritage and conservation areas', 'Techniques sympathetic to the building', 'Layout changes for better spaces', 'Structural changes and modernisation']),
    dict(id='property-development', icon='property', name='Property Development', img='cinema-building-exterior',
         short='We are actively seeking properties and land with development potential across the Caribbean.',
         body=['We are actively seeking properties with development potential, as well as land that may offer the opportunity for new-build projects, particularly in Caribbean countries.',
               'Our aim is to produce unique and interesting properties built with care. If you have a property or land you would like to discuss, please get in touch.'],
         checks=['Properties with development potential', 'Land for new-build projects', 'Projects across the Caribbean', 'Unique properties, built with care']),
    dict(id='ac-service', icon='ac', name='AC Service & Maintenance', img='compressor-room',
         short='Annual maintenance plans that help your air conditioning last longer, with priority service for members.',
         body=['Maintaining your air conditioner helps your unit last longer, and some manufacturer and repair warranties require annual system maintenance to remain valid.',
               'We offer a range of annual maintenance plans to fit different budgets and needs. Our plans also include member perks, such as priority service and discounts on products and repairs.'],
         checks=['Annual plans for a range of budgets', 'Helps keep warranties valid', 'Priority service for plan members', 'Discounts on products and repairs']),
    dict(id='pool-service', icon='pool', name='Pool Service', img=None,
         short='Skilled pool technicians, the latest treatment solutions and a maintenance schedule built around you.',
         body=['When you hire our pool technicians, you can trust that the job will be done right the first time. Our team is highly skilled, trained and experienced enough to handle even the most intricate projects.',
               'We use the latest technology and treatment solutions, so every project is completed as effectively as possible. We can also create a customised pool maintenance schedule to fit your lifestyle.'],
         checks=['Skilled, trained and experienced technicians', 'Latest technology and treatment solutions', 'Customised maintenance schedules', 'Done right the first time']),
]

FAQ = [
    ('What kind of construction projects does GCMC take on?',
     'GCMC takes on small to medium-sized commercial projects, including office and restaurant refurbishments, extensions, small industrial units, change of use and hard landscaping. We also handle renovations and tenant improvements across retail, office, hotel, education and institutional buildings.'),
    ('Where does GCMC work?',
     'GCMC is based in Georgetown, Guyana, and works on general contracting and construction management projects across the Caribbean.'),
    ('Will I have one point of contact during my project?',
     'Yes. We assemble a custom team for every project, large or small, but you always have one contact who makes sure your project needs are being met.'),
    ('Can GCMC renovate older or heritage buildings?',
     'Yes. We have significant experience with listed buildings and buildings in heritage and conservation areas, and we use building techniques that are sympathetic to the original structure.'),
    ('Do you offer air conditioning maintenance plans?',
     'Yes. We offer annual AC maintenance plans for a range of budgets. Plan members get priority service and discounts on products and repairs, and regular maintenance can help keep warranties valid.'),
    ('Do you service swimming pools?',
     'Yes. Our pool technicians use the latest technology and treatment solutions, and we can create a customised pool maintenance schedule to fit your lifestyle.'),
    ('How do I get a quote from GCMC?',
     f'Call us on {PHONE}, email {EMAIL}, or send your project details through the contact form on this website and we will be delighted to quote for your project.'),
]

NAV = [('/', 'Home'), ('/about', 'About'), ('/services', 'Services'), ('/projects/', 'Projects'), ('/contact', 'Contact')]

ORG = {
    '@context': 'https://schema.org',
    '@type': 'GeneralContractor',
    '@id': f'{SITE}/#business',
    'name': 'Global Construction Management',
    'alternateName': 'GCMC',
    'url': f'{SITE}/',
    'logo': f'{SITE}/assets/img/gcmc-logo.png',
    'image': f'{SITE}/assets/img/og-gcmc.jpg',
    'description': 'General contractor and construction management firm in Georgetown, Guyana, offering general construction, building renovation, property development, AC service and pool service across the Caribbean.',
    'telephone': PHONE,
    'email': EMAIL,
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Georgetown', 'addressCountry': 'GY'},
    'areaServed': [{'@type': 'Country', 'name': 'Guyana'}, {'@type': 'Place', 'name': 'Caribbean'}],
    'knowsAbout': [s['name'] for s in SERVICES],
    'hasOfferCatalog': {
        '@type': 'OfferCatalog', 'name': 'Construction services',
        'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['name'], 'description': s['short'], 'url': f'{SITE}/services#{s["id"]}'}} for s in SERVICES],
    },
}

def crumbs(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p} for i, (p, n) in enumerate(items)]}

INTRO_SCRIPT = ("<script>try{if(!sessionStorage.getItem('gcmc-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches)"
                "{document.documentElement.classList.add('show-intro');sessionStorage.setItem('gcmc-intro','1')}}catch(e){}</script>")

def head(path, title, desc, schema, preload=None, noindex=False, extra=''):
    url = SITE + path
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    pre = ''
    if preload:
        m = preload
        big = f', /assets/img/work/{m}-2400.webp 2400w' if m == 'cinema-lobby-blue-lighting' else ''
        pre = (f'<link rel="preload" as="image" href="/assets/img/work/{m}-1600.webp" '
               f'imagesrcset="/assets/img/work/{m}-800.webp 800w, /assets/img/work/{m}-1600.webp 1600w{big}" imagesizes="100vw" fetchpriority="high">\n')
    robots = 'noindex' if noindex else 'index, follow, max-image-preview:large'
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0d141c">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Global Construction Management (GCMC)">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-gcmc.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GY">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/icon-32.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/archivo-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-var-latin.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="/assets/css/style.css?v={CSS_V}">
{INTRO_SCRIPT}
<script src="/assets/js/main.js?v={JS_V}" defer></script>
{extra}{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="intro" aria-hidden="true"><div class="intro__mark"><img src="/assets/img/gcmc-logo-light.webp" width="400" height="111" alt=""></div></div>
'''

def header(active):
    def cur(p):
        return ' aria-current="page"' if p == active else ''
    links = '\n'.join(f'<li><a class="nav__link" href="{p}"{cur(p)}>{n}</a></li>' for p, n in NAV)
    mlinks = '\n'.join(f'<li><a href="{p}"{cur(p)}><small>0{i+1}</small>{n}</a></li>' for i, (p, n) in enumerate(NAV))
    return f'''<header class="header">
  <div class="container header__inner">
    <a class="logo" href="/" aria-label="GCMC, Global Construction Management, home">
      <img class="logo--light" src="/assets/img/gcmc-logo-light.webp" width="400" height="111" alt="">
      <img class="logo--dark" src="/assets/img/gcmc-logo.webp" width="400" height="111" alt="">
    </a>
    <nav class="nav" aria-label="Main">
      <ul class="nav__list">
{links}
      </ul>
    </nav>
    <a class="btn btn--ghost btn--sm header__cta" href="tel:{TEL}">{small_icon("phone")} {PHONE}</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <nav aria-label="Mobile">
    <ul class="mobile-menu__list">
{mlinks}
    </ul>
  </nav>
  <div class="mobile-menu__foot">
    <a href="tel:{TEL}">{PHONE}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <span>Georgetown, Guyana</span>
  </div>
</div>
'''

def mobile_bar(on_contact=False):
    second = (f'<a class="mobile-bar__btn" href="mailto:{EMAIL}">{small_icon("mail")} Email us</a>' if on_contact
              else f'<a class="mobile-bar__btn mobile-bar__btn--primary" href="/contact">Get a quote {ARROW_S}</a>')
    return f'''<div class="mobile-bar" aria-label="Quick contact">
  <a class="mobile-bar__btn" href="tel:{TEL}">{small_icon("phone")} Call</a>
  {second}
</div>
'''

def footer(on_contact=False):
    svc = '\n'.join(f'<li><a href="/services#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
    nav = '\n'.join(f'<li><a href="{p}">{n}</a></li>' for p, n in NAV)
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <img class="footer__logo" src="/assets/img/gcmc-logo-light.webp" width="400" height="111" alt="GCMC, Global Construction Management" loading="lazy">
        <p>A general contracting and construction management firm in Georgetown, Guyana, building with care across the Caribbean.</p>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
{nav}
        </ul>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
{svc}
        </ul>
      </div>
      <div class="footer__contact">
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Georgetown, Guyana</li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>&copy; <span data-year>2026</span> Global Construction Management (GCMC). All rights reserved.</span>
      <span>Website by <a href="https://in2ition.media/" target="_blank" rel="noopener">In2ition Media</a></span>
    </div>
  </div>
  <div class="footer__big" aria-hidden="true">GCMC</div>
</footer>
{mobile_bar(on_contact)}</body>
</html>
'''

def cta(bg='lobby-panorama'):
    return f'''<section class="cta" aria-labelledby="cta-title">
  <div class="cta__bg">{img(bg, parallax="0.12", alt="")}</div>
  <div class="container">
    <p class="eyebrow on-dark" data-reveal>Start your project</p>
    <h2 class="h-lg" id="cta-title" data-split>We'd love to hear <em>from you.</em></h2>
    <p data-reveal style="--d:.2s">We look forward to working with clients who have an eye for detail and a love of high quality. If you're searching for a professional builder, we'd be delighted to quote for your project.</p>
    <div class="cta__actions" data-reveal style="--d:.3s">
      <a class="btn btn--light" href="/contact" data-magnetic>Request a quote {ARROW}</a>
      <a class="btn btn--ghost" href="tel:{TEL}" data-magnetic>Call {PHONE}</a>
    </div>
  </div>
</section>
'''

def page_hero(trail, eyebrow, h1, sub, bg):
    items = '<li><a href="/">Home</a></li>' + ''.join(
        f'<li><a href="{p}">{n}</a></li>' if p else f'<li aria-current="page">{n}</li>' for p, n in trail)
    return f'''<section class="page-hero">
  <div class="page-hero__media" data-parallax="0.18">{img(bg, lazy=False, alt="")}</div>
  <div class="container page-hero__content">
    <ol class="breadcrumb" aria-label="Breadcrumb">{items}</ol>
    <p class="eyebrow on-dark hero__fade" style="--d:.2s">{eyebrow}</p>
    <h1 class="h-xl" data-split>{h1}</h1>
    <p class="hero__fade" style="--d:.7s">{sub}</p>
  </div>
</section>
'''

def video_block(caption=True):
    cap = ('<p class="video-caption">Footage from a commercial fit-out build, March 2021.</p>' if caption else '')
    return f'''<div class="video-block" data-reveal>
  <video class="video-block__main" preload="none" playsinline width="848" height="480" poster="/assets/img/video-poster.webp" aria-label="Video of the GCMC crew on site">
    <source src="/assets/video/gcmc-on-site.mp4" type="video/mp4">
  </video>
  <div class="video-block__poster">
    <video class="video-block__loop" muted loop playsinline preload="none" poster="/assets/img/video-poster.webp" aria-hidden="true" tabindex="-1">
      <source src="/assets/video/gcmc-on-site-loop.mp4" type="video/mp4">
    </video>
  </div>
  <button class="play-btn" type="button" aria-label="Play the GCMC video with sound"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4l14 8-14 8z"/></svg></button>
</div>
{cap}'''

def before_after(before='lobby-under-construction', after='lobby-finished-wide'):
    return f'''<figure class="compare" data-reveal style="--pos:50%">
  <div class="compare__frame">
    {img(before, sizes="(min-width:1320px) 1200px, 100vw", alt="")}
    <div class="compare__after">{img(after, sizes="(min-width:1320px) 1200px, 100vw", alt="")}</div>
    <span class="compare__label compare__label--before">Mid-build</span>
    <span class="compare__label compare__label--after">Finished</span>
    <div class="compare__handle" aria-hidden="true"><span>{ARROW_L}{ARROW_S}</span></div>
    <input class="compare__range" type="range" min="0" max="100" value="50" aria-label="Drag to compare the lobby mid-build and finished">
  </div>
  <figcaption>The same lobby mid-build and finished. Drag the handle to compare.</figcaption>
</figure>'''

def service_cards():
    out = []
    for i, s in enumerate(SERVICES):
        bg = f'<div class="service-card__bg">{img(s["img"], sizes="(min-width:1080px) 33vw, (min-width:680px) 50vw, 100vw", alt="")}</div>' if s['img'] else ''
        out.append(f'''<a class="service-card" href="/services#{s["id"]}" data-reveal style="--d:{(i % 3) * .1:.1f}s">
  {bg}
  <div class="service-card__top">{icon(ICONS[s["icon"]], "service-card__icon")}<span class="service-card__num">0{i+1}</span></div>
  <h3>{s["name"]}</h3>
  <p>{s["short"]}</p>
  <span class="service-card__more">Learn more {ARROW_S}</span>
</a>''')
    return '\n'.join(out)

def case_cards(exclude=None):
    out = []
    for i, (k, c) in enumerate((k, c) for k, c in CASES.items() if k != exclude):
        n = sum(1 for m in MAN.values() if m['cat'] in c['cats'])
        out.append(f'''<a class="case-card" href="/projects/{k}" data-reveal style="--d:{i * .12:.2f}s">
  <div class="img-frame img-frame--wide" data-tilt>{img(c["card"], sizes="(min-width:900px) 50vw, 100vw")}</div>
  <div class="case-card__body">
    <span class="case-card__meta">Case study &middot; {n} photos</span>
    <h3>{c["title"]}</h3>
    <p>{c["summary"]}</p>
    <span class="link-arrow">View project {ARROW_S}</span>
  </div>
</a>''')
    return '\n'.join(out)

LIGHTBOX = f'''<div class="lightbox" role="dialog" aria-modal="true" aria-label="Project image viewer" aria-hidden="true">
  <div class="lightbox__top"><span class="lightbox__count"></span><button class="lb-btn lb-close" type="button" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
  <div class="lightbox__stage">
    <button class="lb-btn lb-prev" type="button" aria-label="Previous image">{ARROW_L}</button>
    <img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="">
    <button class="lb-btn lb-next" type="button" aria-label="Next image">{ARROW_S}</button>
  </div>
  <p class="lightbox__cap" aria-live="polite"></p>
</div>'''

def tiles(items):
    return '\n'.join(f'''<li class="tile" data-cat="{m["cat"]}">
  <button type="button" data-full="/assets/img/work/{m["slug"]}-1600.webp" aria-label="Enlarge: {esc(m["alt"])}">
    {img(m["slug"], sizes="(min-width:1040px) 33vw, (min-width:620px) 50vw, 100vw")}
    <span class="tile__cap"><small>{CATS[m["cat"]]}</small><strong>{title_of(m["slug"])}</strong></span>
  </button>
</li>''' for m in items)

def write(name, content):
    path = ROOT + name
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# ================= HOME =================
HERO = [
    ('cinema-lobby-blue-lighting', 'Commercial fit-out · lobby & concessions'),
    ('cinema-auditorium-screen', 'Commercial fit-out · auditorium'),
    ('living-room-renovation', 'Residential renovation · living space'),
    ('upper-level-escalator', 'Commercial fit-out · upper level'),
]
slides = '\n'.join(
    f'<div class="hero__slide{" is-active" if i == 0 else ""}" data-caption="{esc(c)}">{img(s, lazy=(i != 0), alt="" if i else MAN[s]["alt"])}</div>'
    for i, (s, c) in enumerate(HERO))
dots = '\n'.join(f'<button type="button" aria-label="Show image {i+1} of {len(HERO)}"></button>' for i in range(len(HERO)))
RAIL = ['cinema-lobby-purple-lighting', 'living-room-renovation', 'cinema-auditorium-screen', 'curved-bulkhead-drywall',
        'open-plan-kitchen', 'concession-counter', 'ups-power-room', 'bathroom-shower', 'cinema-building-exterior']
rail = '\n'.join(f'''<li class="rail__item">
  <a href="/projects/{case_for(MAN[s]["cat"])}">
    <div class="img-frame" data-tilt>{img(s, sizes="(min-width:1000px) 520px, 82vw")}</div>
    <div class="rail__cap"><strong>{title_of(s)}</strong><span>{CATS[MAN[s]["cat"]]}</span></div>
  </a>
</li>''' for s in RAIL)
marquee_items = ''.join(f'<span class="marquee__item">{s["name"]}</span>' for s in SERVICES)

home = head('/', 'GCMC | Construction Company & Contractor in Georgetown, Guyana',
            'GCMC is a general contractor in Georgetown, Guyana, offering commercial construction, renovations, construction management, AC service and pool service.',
            [ORG, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Global Construction Management (GCMC)', 'url': f'{SITE}/'}],
            preload='cinema-lobby-blue-lighting') + header('/') + f'''<main id="main">
<section class="hero" aria-label="Introduction">
  <div class="hero__slides">
{slides}
  </div>
  <div class="container hero__content">
    <p class="eyebrow hero__eyebrow hero__fade" style="--d:.2s">General contractor &middot; Georgetown, Guyana</p>
    <h1 class="h-xl" data-split>We have a wealth of building <em>experience.</em></h1>
    <p class="hero__sub hero__fade" style="--d:.9s">&hellip;and we're not afraid to use it. GCMC delivers commercial construction, renovations and construction management across Guyana and the Caribbean, with excellence in on-site management on every job.</p>
    <div class="hero__actions hero__fade" style="--d:1.1s">
      <a class="btn btn--light" href="/projects/" data-magnetic>See our work {ARROW}</a>
      <a class="btn btn--ghost" href="/contact" data-magnetic>Request a quote</a>
    </div>
    <div class="hero__bar hero__fade" style="--d:1.3s">
      <button class="hero__pause" type="button" aria-label="Pause slideshow" aria-pressed="false"><span class="hero__pause-icon hero__pause-icon--pause">{small_icon("pause")}</span><span class="hero__pause-icon hero__pause-icon--play">{small_icon("play")}</span></button>
      <div class="hero__progress" role="group" aria-label="Slideshow">
{dots}
      </div>
      <p class="hero__caption" aria-live="polite"></p>
      <span class="scroll-cue" aria-hidden="true"><i></i>Scroll</span>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    <div class="marquee__group">{marquee_items}</div>
    <div class="marquee__group">{marquee_items}</div>
  </div>
</div>

<section class="section" aria-labelledby="intro-title">
  <div class="container split split--wide-text">
    <div>
      <p class="eyebrow" data-reveal>At GCMC</p>
      <h2 class="h-lg" id="intro-title" data-split>The expertise of a large firm, <em>the care of a boutique one.</em></h2>
      <p class="lead" data-reveal style="--d:.15s;margin-top:28px">GCMC has worked across many industries, and we know the intricacies of retail, office, hotel, education and institutional projects. We understand the needs of business owners, contractors, brokers, developers and landlords.</p>
      <ul class="chips" data-reveal style="--d:.25s">
        <li>Retail</li><li>Office</li><li>Hotels</li><li>Education</li><li>Institutional</li><li>New construction</li><li>Renovations</li><li>Tenant improvements</li>
      </ul>
      <div class="stats" data-reveal style="--d:.3s">
        <div class="stat"><div class="stat__num"><span data-count="10">10</span><sup>+</sup></div><div class="stat__label">Years of trusted experience</div></div>
        <div class="stat"><div class="stat__num"><span data-count="6">6</span></div><div class="stat__label">Core building &amp; property services</div></div>
        <div class="stat"><div class="stat__num"><span data-count="1">1</span></div><div class="stat__label">Point of contact on every project</div></div>
      </div>
    </div>
    <div class="split__media">
      <div class="img-frame img-frame--tall" data-reveal="clip">{img("lobby-under-construction", sizes="(min-width:960px) 42vw, 100vw")}</div>
      <div class="badge-card" data-reveal style="--d:.5s"><strong>Top-down</strong><span>Principals and directors involved from first estimate to final finish.</span></div>
    </div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="services-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>What we do</p>
        <h2 class="h-lg" id="services-title" data-split>Building and property services, <em>under one roof.</em></h2>
      </div>
      <div data-reveal style="--d:.2s">
        <p class="lead">From ground-up commercial builds to the maintenance that keeps buildings running, one experienced team handles it all.</p>
        <a class="link-arrow" href="/services" style="margin-top:18px">All services {ARROW_S}</a>
      </div>
    </div>
    <div class="services-grid">
{service_cards()}
    </div>
  </div>
</section>

<section class="rail-section section" aria-labelledby="work-title">
  <div class="rail-sticky">
    <div class="container section-head" style="margin-bottom:clamp(32px,4vw,56px)">
      <div>
        <p class="eyebrow" data-reveal>Our work</p>
        <h2 class="h-lg" id="work-title" data-split>Take a look at our <em>recent projects.</em></h2>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;--d:.2s" data-reveal>
        <a class="link-arrow" href="/projects/">View all projects {ARROW_S}</a>
        <div class="rail-controls">
          <button type="button" data-dir="prev" aria-label="Previous projects">{ARROW_L}</button>
          <button type="button" data-dir="next" aria-label="Next projects">{ARROW_S}</button>
        </div>
      </div>
    </div>
    <ul class="rail">
{rail}
    </ul>
    <div class="rail-progress" aria-hidden="true"><span></span></div>
  </div>
</section>

<section class="section section--white" aria-labelledby="compare-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>From shell to finished</p>
        <h2 class="h-lg" id="compare-title" data-split>See the difference <em>we make.</em></h2>
      </div>
      <div data-reveal style="--d:.2s">
        <p class="lead muted">A commercial lobby, mid-build and ready to open. Every curve, colour and light fitting was framed, finished and fitted on site.</p>
        <a class="link-arrow" href="/projects/cinema-fit-out" style="margin-top:18px">See the full build {ARROW_S}</a>
      </div>
    </div>
    {before_after()}
  </div>
</section>

<section class="section" aria-labelledby="approach-title">
  <div class="container split split--top">
    <div class="split__media">
      <div class="sticky-media">
        <div class="img-frame img-frame--tall" data-reveal="clip">{img("site-walkthrough", sizes="(min-width:960px) 45vw, 100vw")}</div>
      </div>
    </div>
    <div>
      <p class="eyebrow" data-reveal>How we work</p>
      <h2 class="h-lg" id="approach-title" data-split>Solid construction. <em>Excellent on-site management.</em></h2>
      <p class="lead muted" data-reveal style="--d:.15s;margin:28px 0 40px">These are the cornerstones of our business, and they shape how every GCMC project runs.</p>
      <div class="principles">
        <div class="principle" data-reveal><div><h3>Top-down involvement</h3><p>Principals and directors work alongside project managers, estimators, supervisors and our labourers on site, on projects small and large.</p></div></div>
        <div class="principle" data-reveal style="--d:.08s"><div><h3>A custom team for every project</h3><p>We assemble the right team to tackle any project, large or small, so you get the people your project actually needs.</p></div></div>
        <div class="principle" data-reveal style="--d:.16s"><div><h3>One point of contact</h3><p>However big the team, you always have one contact who makes sure your project needs are being met.</p></div></div>
        <div class="principle" data-reveal style="--d:.24s"><div><h3>Large-firm capability, boutique care</h3><p>The expertise and full capabilities of a large firm, with the attention to detail of a boutique one.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="video-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>On site</p>
        <h2 class="h-lg" id="video-title" data-split>See GCMC <em>at work.</em></h2>
      </div>
      <p class="lead" data-reveal style="--d:.2s">Our crew framing, fixing and finishing on a commercial fit-out. Press play for the full film with sound.</p>
    </div>
    {video_block()}
  </div>
</section>
</main>
''' + cta() + footer()
write('index.html', home)

# ================= SERVICES =================
details = []
for i, s in enumerate(SERVICES):
    if s['img']:
        media = f'<div class="img-frame img-frame--tall" data-reveal="clip">{img(s["img"], sizes="(min-width:960px) 45vw, 100vw")}</div>'
    else:
        media = f'''<div class="water-panel" data-reveal role="img" aria-label="Illustration of a swimming pool">
  {icon(ICONS["pool"], "water-icon")}
  <svg class="waves" viewBox="0 0 800 200" preserveAspectRatio="none" aria-hidden="true"><path d="M0 80 Q100 40 200 80 T400 80 T600 80 T800 80 V200 H0Z" fill="rgba(255,255,255,.18)"/><path d="M0 110 Q100 70 200 110 T400 110 T600 110 T800 110 V200 H0Z" fill="rgba(255,255,255,.14)"/></svg>
</div>'''
    body = ''.join(f'<p class="{"lead" if j == 0 else "muted"}">{p}</p>' for j, p in enumerate(s['body']))
    checks = ''.join(f'<li>{c}</li>' for c in s['checks'])
    ask = 'AC service' if s['id'] == 'ac-service' else s['name'].lower()
    details.append(f'''<article class="service-detail" id="{s["id"]}">
  <div class="service-detail__media">{media}</div>
  <div>
    <p class="service-detail__num" data-reveal>{icon(ICONS[s["icon"]])} 0{i+1} / 06</p>
    <h2 class="h-lg" data-split>{s["name"]}</h2>
    <div data-reveal style="--d:.15s">{body}</div>
    <ul class="checklist" data-reveal style="--d:.25s">{checks}</ul>
    <a class="btn btn--ghost-dark" href="/contact?service={s["id"]}" style="margin-top:34px" data-reveal>Ask about {ask} {ARROW}</a>
  </div>
</article>''')
subnav = ''.join(f'<li><a href="#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
faq_html = '\n'.join(f'<details data-reveal style="--d:{i*.05:.2f}s"><summary>{q}<i aria-hidden="true"></i></summary><div class="faq__body"><p>{a}</p></div></details>' for i, (q, a) in enumerate(FAQ))
faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
services = head('/services', 'Construction Services in Guyana | GCMC',
                'Commercial construction, construction management, building renovation, property development, AC maintenance and pool service from GCMC in Georgetown, Guyana.',
                [ORG, crumbs([('/', 'Home'), ('/services', 'Services')]), faq_ld], preload='upper-level-escalator') + header('/services') + f'''<main id="main">
{page_hero([(None, "Services")], "What we do", "Construction services <em>in Guyana.</em>", "Six services, one experienced team. From commercial builds and renovations to the maintenance that keeps your property running.", "upper-level-escalator")}
<nav class="subnav" aria-label="Services"><div class="container"><ul>{subnav}</ul></div></nav>
<div class="container">
{chr(10).join(details)}
</div>
<section class="section" aria-labelledby="faq-title">
  <div class="container split split--wide-text split--top">
    <div class="faq">
{faq_html}
    </div>
    <div class="sticky-media">
      <p class="eyebrow" data-reveal>FAQ</p>
      <h2 class="h-lg" id="faq-title" data-split>Questions, <em>answered.</em></h2>
      <p class="lead muted" data-reveal style="--d:.15s;margin-top:24px">Can't find what you're looking for? Call <a href="tel:{TEL}" style="color:var(--ink);font-weight:600">{PHONE}</a> and we'll talk it through.</p>
    </div>
  </div>
</section>
</main>
''' + cta('cinema-lobby-purple-lighting') + footer()
write('services.html', services)

# ================= PROJECTS (index) =================
order = ['commercial', 'construction', 'residential', 'mep']
items = sorted(MAN.values(), key=lambda m: order.index(m['cat']))
counts = {c: sum(1 for m in items if m['cat'] == c) for c in order}
filters = f'<button type="button" class="filter-btn" data-filter="all" aria-pressed="true">All<span>{len(items)}</span></button>' + ''.join(
    f'<button type="button" class="filter-btn" data-filter="{c}" aria-pressed="false">{CATS[c]}<span>{counts[c]}</span></button>' for c in order)
gallery_ld = {'@context': 'https://schema.org', '@type': 'ImageGallery', 'name': 'GCMC project gallery', 'url': f'{SITE}/projects/',
              'image': [{'@type': 'ImageObject', 'contentUrl': f'{SITE}/assets/img/work/{m["slug"]}-1600.webp', 'description': m['alt']} for m in items]}
projects = head('/projects/', 'Our Work | Construction Projects in Guyana | GCMC',
                'Browse GCMC construction projects in Guyana: commercial fit-outs, construction in progress, residential renovations and mechanical and electrical installs.',
                [ORG, crumbs([('/', 'Home'), ('/projects/', 'Projects')]), gallery_ld], preload='cinema-lobby-purple-lighting') + header('/projects/') + f'''<main id="main">
{page_hero([(None, "Projects")], "Our work", "Built with care, <em>down to the detail.</em>", "Commercial fit-outs, major remodels and the work behind the walls. Find inspiration for your new build or renovation in our projects.", "cinema-lobby-purple-lighting")}
<section class="section section--tight" aria-labelledby="cases-title">
  <div class="container">
    <div class="section-head" style="margin-bottom:40px">
      <div>
        <p class="eyebrow" data-reveal>Case studies</p>
        <h2 class="h-lg" id="cases-title" data-split>Featured <em>projects.</em></h2>
      </div>
    </div>
    <div class="case-grid">
{case_cards()}
    </div>
  </div>
</section>
<section class="section section--white" aria-labelledby="gallery-title">
  <div class="container">
    <h2 class="h-md" id="gallery-title" style="margin-bottom:28px" data-reveal>Full gallery</h2>
    <div class="filters" role="group" aria-label="Filter projects" data-reveal>{filters}</div>
    <ul class="masonry">
{tiles(items)}
    </ul>
  </div>
</section>
{LIGHTBOX}
</main>
''' + cta('concession-blue-glow') + footer()
write('projects/index.html', projects)

# ================= CASE STUDIES =================
def step(n, title, text, slugs):
    pics = ''.join(f'<div class="img-frame img-frame--wide" data-reveal="clip" style="--d:{i*.12:.2f}s">{img(s, sizes="(min-width:960px) 30vw, 100vw")}</div>' for i, s in enumerate(slugs))
    return f'''<li class="timeline__step">
  <div class="timeline__text" data-reveal><span class="timeline__num">0{n}</span><h3>{title}</h3><p>{text}</p></div>
  <div class="timeline__pics timeline__pics--{len(slugs)}">{pics}</div>
</li>'''

def case_page(key, body, desc):
    c = CASES[key]
    gal = [m for m in items if m['cat'] in c['cats']]
    other = next(k for k in CASES if k != key)
    page = head(f'/projects/{key}', f'{c["title"]} | GCMC Projects, Guyana', desc,
                [ORG, crumbs([('/', 'Home'), ('/projects/', 'Projects'), (f'/projects/{key}', c['title'])])], preload=c['hero']) + header('/projects/') + f'''<main id="main">
{page_hero([("/projects/", "Projects"), (None, c["nav"])], "Case study", c["title"].replace(" & ", " &amp; ", 1).rsplit(" ", 1)[0] + " <em>" + c["title"].rsplit(" ", 1)[1] + ".</em>", c["summary"], c["hero"])}
{body}
<section class="section section--white" aria-labelledby="gallery-title">
  <div class="container">
    <div class="section-head" style="margin-bottom:40px">
      <div>
        <p class="eyebrow" data-reveal>Gallery</p>
        <h2 class="h-lg" id="gallery-title" data-split>Every photo from <em>this project.</em></h2>
      </div>
      <p class="lead muted" data-reveal style="--d:.2s">Select any photo to view it full size.</p>
    </div>
    <ul class="masonry">
{tiles(gal)}
    </ul>
  </div>
</section>
<section class="section section--tight" aria-labelledby="next-title">
  <div class="container">
    <p class="eyebrow" data-reveal>Next project</p>
    <h2 class="visually-hidden" id="next-title">Next project</h2>
    <div class="case-grid case-grid--single">
{case_cards(exclude=key)}
    </div>
  </div>
</section>
{LIGHTBOX}
</main>
''' + cta() + footer()
    write(f'projects/{key}.html', page)

cinema_body = f'''<section class="section" aria-labelledby="overview-title">
  <div class="container split split--wide-text">
    <div>
      <p class="eyebrow" data-reveal>Overview</p>
      <h2 class="h-lg" id="overview-title" data-split>A complete interior, <em>start to finish.</em></h2>
      <p class="lead" data-reveal style="--d:.15s;margin-top:28px">This project took an open steel building shell and turned it into a finished cinema: a lobby with sweeping curved ceilings, concession counters, upper-level circulation, auditoriums with tiered seating, and the power and mechanical rooms that keep it all running.</p>
      <p class="muted" data-reveal style="--d:.2s">It brought together several GCMC services on one site, coordinated by one team from structure to final finishes.</p>
      <ul class="chips" data-reveal style="--d:.25s"><li>General construction</li><li>Construction management</li><li>Interior fit-out</li><li>Mechanical &amp; electrical</li></ul>
    </div>
    <div class="split__media">
      <div class="img-frame img-frame--tall" data-reveal="clip">{img("cinema-auditorium-screen", sizes="(min-width:960px) 40vw, 100vw")}</div>
    </div>
  </div>
</section>
<section class="section section--white" aria-labelledby="build-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>The build</p>
        <h2 class="h-lg" id="build-title" data-split>From shell <em>to showtime.</em></h2>
      </div>
      <p class="lead muted" data-reveal style="--d:.2s">How the space came together, stage by stage.</p>
    </div>
    <ol class="timeline">
{step(1, "Structure &amp; services", "Structural steel and overhead services were set out in the open building shell.", ["site-walkthrough", "structural-steel"])}
{step(2, "Framing", "Steel stud walls went up with insulation, along with the framework for the lobby's sweeping curved ceilings.", ["insulated-stud-walls", "curved-bulkhead-framing"])}
{step(3, "Drywall &amp; ceilings", "The curved bulkheads were boarded and finished, and suspended ceiling grids were installed.", ["curved-bulkhead-drywall", "ceiling-grid-install"])}
{step(4, "Finishes &amp; fit-out", "Floors, feature colours, lighting and the concession counters went in.", ["lobby-under-construction", "concession-counter"])}
{step(5, "Ready to open", "A finished lobby and auditoriums, ready for the first audience.", ["lobby-pink-cove", "cinema-auditorium-screen"])}
    </ol>
  </div>
</section>
<section class="section" aria-labelledby="compare-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>Before &amp; after</p>
        <h2 class="h-lg" id="compare-title" data-split>The same lobby, <em>two stages.</em></h2>
      </div>
    </div>
    {before_after()}
  </div>
</section>
<section class="section section--dark" aria-labelledby="plant-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>Behind the scenes</p>
        <h2 class="h-lg" id="plant-title" data-split>The work <em>behind the walls.</em></h2>
      </div>
      <p class="lead" data-reveal style="--d:.2s">Power, projection and compressed-air systems, installed in dedicated plant rooms.</p>
    </div>
    <div class="plant-grid">
      <div class="img-frame" data-reveal="clip">{img("ups-power-room", sizes="(min-width:900px) 50vw, 100vw")}</div>
      <div class="img-frame" data-reveal="clip" style="--d:.1s">{img("projection-power-equipment", sizes="(min-width:900px) 25vw, 50vw")}</div>
      <div class="img-frame" data-reveal="clip" style="--d:.2s">{img("electrical-panels", sizes="(min-width:900px) 25vw, 50vw")}</div>
      <div class="img-frame" data-reveal="clip" style="--d:.3s">{img("compressor-room", sizes="(min-width:900px) 25vw, 50vw")}</div>
      <div class="img-frame" data-reveal="clip" style="--d:.4s">{img("amplifier-rack", sizes="(min-width:900px) 25vw, 50vw")}</div>
    </div>
  </div>
</section>
<section class="section section--dark" style="padding-top:0" aria-labelledby="film-title">
  <div class="container">
    <h2 class="h-md" id="film-title" style="margin-bottom:28px" data-reveal>On site during the build</h2>
    {video_block()}
  </div>
</section>
'''
case_page('cinema-fit-out', cinema_body,
          'How GCMC took a commercial building shell to a finished cinema in Guyana: structure, framing, curved ceilings, finishes and plant rooms, in photos.')

resi_body = f'''<section class="section" aria-labelledby="overview-title">
  <div class="container split split--wide-text">
    <div>
      <p class="eyebrow" data-reveal>Overview</p>
      <h2 class="h-lg" id="overview-title" data-split>New life for <em>lived-in homes.</em></h2>
      <p class="lead" data-reveal style="--d:.15s;margin-top:28px">Renovation projects breathe new life into tired homes. You can update the layout to create better spaces, make structural changes, or simply modernise what already exists.</p>
      <p class="muted" data-reveal style="--d:.2s">These residential interiors show what that looks like in practice: warm living spaces with feature walls, granite-topped kitchens, and bathrooms finished in large-format tile.</p>
      <ul class="chips" data-reveal style="--d:.25s"><li>Building renovation</li><li>Kitchens</li><li>Bathrooms</li><li>Living spaces</li></ul>
    </div>
    <div class="split__media">
      <div class="img-frame img-frame--tall" data-reveal="clip">{img("living-room-renovation", sizes="(min-width:960px) 40vw, 100vw")}</div>
    </div>
  </div>
</section>
<section class="section section--white" aria-labelledby="rooms-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>Room by room</p>
        <h2 class="h-lg" id="rooms-title" data-split>Designed around <em>how you live.</em></h2>
      </div>
    </div>
    <ol class="timeline">
{step(1, "Living spaces", "Open living areas with stone feature walls, warm colour and comfortable, curved seating.", ["living-room-renovation", "lounge-seating"])}
{step(2, "Kitchens", "Kitchen islands with granite counters, wood cabinetry and range hoods, opening onto dining and living areas.", ["open-plan-kitchen", "kitchen-island-granite"])}
{step(3, "Bathrooms", "Large-format tiles, glass showers, vessel basins and round mirrors for a clean, modern finish.", ["bathroom-shower", "bathroom-vanity"])}
    </ol>
  </div>
</section>
'''
case_page('residential-renovations', resi_body,
          'Residential renovations by GCMC in Guyana: living spaces, kitchens with granite islands and modern tiled bathrooms, in photos.')

# ================= ABOUT =================
SECTORS = [('retail', 'Retail', 'Shops and retail units fitted out to trade.'),
           ('office', 'Office', 'Workplaces, refurbishments and extensions.'),
           ('hotel', 'Hotels', 'Hospitality spaces built to welcome guests.'),
           ('education', 'Education', 'Learning spaces for schools and institutions.'),
           ('institutional', 'Institutional', 'Public and institutional buildings.'),
           ('new', 'New construction', 'Ground-up builds, including small industrial units.'),
           ('renovation', 'Renovations', 'New life for existing and heritage buildings.'),
           ('tenant', 'Tenant improvements', 'Spaces adapted for the people moving in.')]
sectors = '\n'.join(f'<div class="sector" data-reveal style="--d:{(i % 4) * .07:.2f}s">{icon(ICONS[k])}<h3>{t}</h3><p>{d}</p></div>' for i, (k, t, d) in enumerate(SECTORS))
about = head('/about', 'About GCMC | General Contractor in Georgetown, Guyana',
             'GCMC brings over a decade of general contracting and construction management experience to projects in Guyana and the Caribbean, with one point of contact.',
             [ORG, crumbs([('/', 'Home'), ('/about', 'About')])], preload='open-plan-kitchen') + header('/about') + f'''<main id="main">
{page_hero([(None, "About")], "About GCMC", "Over a decade of <em>trusted experience.</em>", "A general contracting and construction management firm in Georgetown, Guyana, with a boutique approach and top-down involvement on every project.", "open-plan-kitchen")}
<section class="section" aria-labelledby="story-title">
  <div class="container split">
    <div>
      <p class="eyebrow" data-reveal>Our story</p>
      <h2 class="h-lg" id="story-title" data-split>One of the Caribbean's <em>trusted contractors.</em></h2>
      <p class="lead" data-reveal style="--d:.15s;margin-top:28px">With over a decade of trusted experience, GCMC has grown to become one of the top general contracting and construction management firms in the Caribbean.</p>
      <p class="muted" data-reveal style="--d:.2s">The cornerstones of our business are solid construction and excellence in on-site management. We bring our clients the expertise and full capabilities of a large firm, while keeping a boutique approach with top-down involvement.</p>
      <p class="muted" data-reveal style="--d:.25s">That means our teams work together on every project, small and large, from principals and directors to project managers, estimators, supervisors and our labourers on site.</p>
    </div>
    <div class="collage">
      <div class="img-frame" data-reveal="clip">{img("cinema-lobby-blue-lighting", sizes="(min-width:960px) 32vw, 66vw")}</div>
      <div class="img-frame" data-reveal="clip" style="--d:.15s">{img("steel-framing-ceiling", sizes="(min-width:960px) 16vw, 33vw")}</div>
      <div class="img-frame" data-reveal="clip" style="--d:.25s">{img("kitchen-island-granite", sizes="(min-width:960px) 16vw, 33vw")}</div>
      <div class="img-frame" data-reveal="clip" style="--d:.35s">{img("electrical-panels", sizes="(min-width:960px) 24vw, 50vw")}</div>
    </div>
  </div>
</section>

<section class="section section--dark" aria-label="Our promise">
  <div class="container split">
    <p class="quote" data-split>"However large the team, you will always have <em>one contact</em> making sure your project needs are met."</p>
    <div data-reveal style="--d:.2s">
      <p class="lead">We have the ability to assemble a custom team to tackle any project, large or small. We understand the needs of business owners, contractors, brokers, developers and landlords, and we build our team around yours.</p>
      <a class="btn btn--light" href="/contact" style="margin-top:28px" data-magnetic>Talk to us {ARROW}</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="sectors-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>Experience</p>
        <h2 class="h-lg" id="sectors-title" data-split>We know the intricacies <em>of every sector.</em></h2>
      </div>
      <p class="lead muted" data-reveal style="--d:.2s">GCMC has worked across many industries, on new construction, renovations and tenant improvements.</p>
    </div>
    <div class="sectors">
{sectors}
    </div>
  </div>
</section>

<section class="section section--white" aria-labelledby="video-title">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow" data-reveal>On site</p>
        <h2 class="h-lg" id="video-title" data-split>See GCMC <em>at work.</em></h2>
      </div>
      <p class="lead muted" data-reveal style="--d:.2s">Our crew framing, fixing and finishing on a commercial fit-out.</p>
    </div>
    {video_block()}
  </div>
</section>
</main>
''' + cta('lobby-finished-wide') + footer()
write('about.html', about)

# ================= CONTACT =================
opts = ''.join(f'<option value="{s["name"]}" data-id="{s["id"]}">{s["name"]}</option>' for s in SERVICES)
contact_ld = {'@context': 'https://schema.org', '@type': 'ContactPage', 'name': 'Contact GCMC', 'url': f'{SITE}/contact', 'about': {'@id': f'{SITE}/#business'}}
contact = head('/contact', 'Contact GCMC | Get a Construction Quote in Guyana',
               f'Contact Global Construction Management (GCMC) in Georgetown, Guyana for a construction or renovation quote. Call {PHONE} or email {EMAIL}.',
               [ORG, crumbs([('/', 'Home'), ('/contact', 'Contact')]), contact_ld], preload='lobby-pink-cove',
               extra='<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>\n') + header('/contact') + f'''<main id="main">
{page_hero([(None, "Contact")], "Contact us", "Let's build <em>something great.</em>", "Tell us about your project. If you're searching for a professional builder, we'd be delighted to quote for it.", "lobby-pink-cove")}
<section class="section" aria-labelledby="contact-title">
  <div class="container">
    <div class="contact-grid">
      <div>
        <p class="eyebrow" data-reveal>Get in touch</p>
        <h2 class="h-lg" id="contact-title" data-split>We'd love to <em>hear from you.</em></h2>
        <p class="lead muted" data-reveal style="--d:.15s;margin-top:24px">We look forward to working with clients who have an eye for detail and a love of high quality.</p>
        <div class="contact-cards" data-reveal style="--d:.25s">
          <a class="contact-card" href="tel:{TEL}"><span class="contact-card__icon">{small_icon("phone")}</span><span><small>Call us</small><strong>{PHONE}</strong></span></a>
          <a class="contact-card" href="mailto:{EMAIL}"><span class="contact-card__icon">{small_icon("mail")}</span><span><small>Email us</small><strong>{EMAIL}</strong></span></a>
          <div class="contact-card"><span class="contact-card__icon">{small_icon("pin")}</span><span><small>Based in</small><strong>Georgetown, Guyana</strong></span></div>
        </div>
      </div>
      <form class="form" id="quote-form" action="/api/contact" method="post" data-to="{EMAIL}" novalidate data-reveal style="--d:.2s">
        <h3 class="h-md" style="margin-bottom:28px">Request a quote</h3>
        <div class="form__row form__row--2">
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" maxlength="120" required><span class="error">Please enter your name.</span></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" maxlength="200" required><span class="error">Please enter a valid email address.</span></div>
        </div>
        <div class="form__row form__row--2">
          <div class="field"><label for="f-phone">Phone <span class="muted">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="60"></div>
          <div class="field"><label for="f-service">Service</label><select id="f-service" name="service"><option value="">Choose a service</option>{opts}<option value="Other">Something else</option></select></div>
        </div>
        <div class="field"><label for="f-message">Tell us about your project</label><textarea id="f-message" name="message" maxlength="5000" required></textarea><span class="error">Please tell us a little about your project.</span></div>
        <div class="field field--hp" aria-hidden="true"><label for="f-website">Leave this empty</label><input id="f-website" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="cf-turnstile" data-sitekey="{TURNSTILE_SITE_KEY}" data-theme="light" data-size="flexible"></div>
        <button class="btn" type="submit" data-magnetic><span class="btn__label">Send enquiry</span> {ARROW}</button>
        <p class="form__status" role="status" aria-live="polite"></p>
        <p class="form__note">We usually reply within one working day. Prefer to talk? Call <a href="tel:{TEL}">{PHONE}</a>.</p>
      </form>
    </div>
    <div class="map" data-reveal>
      <iframe title="Map of Georgetown, Guyana" src="https://www.google.com/maps?q=Georgetown,+Guyana&amp;z=13&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>
</main>
''' + footer(on_contact=True)
write('contact.html', contact)

# ================= 404 =================
nf = head('/404', 'Page not found | GCMC', 'This page could not be found.', [], noindex=True) + f'''<main id="main" class="notfound">
  <div>
    <h1>404</h1>
    <p style="margin:18px 0 32px">This page is still under construction, or it has moved.</p>
    <a class="btn btn--light" href="/">Back to home {ARROW}</a>
  </div>
</main>
</body>
</html>
'''
write('404.html', nf)

# ================= robots, sitemap, manifest, llms =================
write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
paths = [p for p, _ in NAV] + [f'/projects/{k}' for k in CASES]
urls = ''.join(f'  <url><loc>{SITE}{p}</loc><lastmod>{LASTMOD}</lastmod></url>\n' for p in paths)
write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
write('site.webmanifest', json.dumps({'name': 'Global Construction Management (GCMC)', 'short_name': 'GCMC', 'start_url': '/', 'display': 'standalone',
                                      'background_color': '#0d141c', 'theme_color': '#0d141c',
                                      'icons': [{'src': '/assets/img/icon-180.png', 'sizes': '180x180', 'type': 'image/png'}, {'src': '/assets/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=2))
write('llms.txt', f'''# Global Construction Management (GCMC)

> GCMC is a general contracting and construction management firm based in Georgetown, Guyana, with over a decade of experience on projects across the Caribbean.

- Phone: {PHONE}
- Email: {EMAIL}
- Location: Georgetown, Guyana

## Services
''' + ''.join(f'- [{s["name"]}]({SITE}/services#{s["id"]}): {s["short"]}\n' for s in SERVICES) + f'''
## Projects
''' + ''.join(f'- [{c["title"]}]({SITE}/projects/{k}): {c["summary"]}\n' for k, c in CASES.items()) + f'''
## Pages
- [About]({SITE}/about)
- [All projects]({SITE}/projects/)
- [Contact]({SITE}/contact)
''')
print('built')
