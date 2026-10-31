# GCMC — Global Construction Management website

Static website for gcmcgeo.com, hosted on **Cloudflare Pages** with one Pages Function for the quote form.

```
build.py              Generates every page in site/ from one template file
site/                 The published website (Cloudflare Pages output directory)
  _headers            Caching + security headers
  _redirects          Old site URLs → new pages
  assets/             CSS, JS, fonts, images (WebP), video
functions/api/contact.js   POST /api/contact: honeypot → Turnstile → Resend email
```

## Editing

Pages are generated, so edit `build.py` (copy, services, FAQ, projects) and run:

```bash
pip install pillow   # once
python3 build.py
```

CSS (`site/assets/css/style.css`) and JS (`site/assets/js/main.js`) are edited directly; re-run `build.py` afterwards so the
`?v=` cache-busting hash in each page updates.

## Local preview

```bash
npx wrangler pages dev site
```

For the form to work locally, create `.dev.vars` (git-ignored):

```
TURNSTILE_SECRET_KEY=1x0000000000000000000000000000000AA
DRY_RUN=1
```

`DRY_RUN=1` logs the email instead of sending it.

## Cloudflare Pages setup

- **Framework preset:** None
- **Build command:** *(leave empty)*
- **Build output directory:** `site`

**Variables and Secrets** (Settings → Variables and Secrets, Production):

| Name | Type | Value |
|---|---|---|
| `TURNSTILE_SECRET_KEY` | Secret | From Cloudflare → Turnstile → your widget |
| `RESEND_API_KEY` | Secret | From resend.com → API Keys |
| `MAIL_TO` | Text | Where enquiries go (default `jleegcmc@gmail.com`) |
| `MAIL_FROM` | Text | Sender on a Resend-verified domain, e.g. `GCMC Website <website@gcmcgeo.com>` |

Before going live:

1. Create a Turnstile widget for `gcmcgeo.com` and put its **site key** in `TURNSTILE_SITE_KEY` at the top of `build.py`
   (it currently uses Cloudflare's always-pass test key), then run `python3 build.py`.
2. Verify `gcmcgeo.com` in Resend (add its DNS records in Cloudflare), or set `MAIL_FROM` to another verified domain.
