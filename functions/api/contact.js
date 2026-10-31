/**
 * POST /api/contact — Cloudflare Pages Function for the quote form.
 *
 * 1. Drops obvious bots (hidden honeypot field).
 * 2. Verifies the Cloudflare Turnstile token server-side.
 * 3. Emails the enquiry via Resend.
 *
 * Variables (Cloudflare → Workers & Pages → this project → Settings → Variables and Secrets):
 *   TURNSTILE_SECRET_KEY  (secret)   Turnstile widget secret key
 *   RESEND_API_KEY        (secret)   Resend API key
 *   MAIL_TO               (optional) where enquiries go, default jleegcmc@gmail.com
 *   MAIL_FROM             (optional) sender on a Resend-verified domain, default "GCMC Website <website@gcmcgeo.com>"
 *   DRY_RUN               (optional) "1" logs the email instead of sending it (local testing)
 */

const LIMITS = { name: 120, email: 200, phone: 60, service: 80, message: 5000 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

const escapeHtml = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export async function onRequestPost({ request, env }) {
  let form;
  try { form = await request.formData(); } catch { return json({ ok: false, error: 'bad-request' }, 400); }

  // Honeypot: real people never see or fill this field. Pretend success so bots don't retry.
  if ((form.get('company_website') || '').toString().trim()) return json({ ok: true });

  // Turnstile verification
  const token = (form.get('cf-turnstile-response') || '').toString();
  if (!token) return json({ ok: false, error: 'verification' }, 400);
  if (!env.TURNSTILE_SECRET_KEY) { console.error('TURNSTILE_SECRET_KEY is not set'); return json({ ok: false, error: 'not-configured' }, 500); }
  const verify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({
      secret: env.TURNSTILE_SECRET_KEY,
      response: token,
      remoteip: request.headers.get('CF-Connecting-IP') || '',
    }),
  }).then((r) => r.json()).catch(() => ({ success: false }));
  if (!verify.success) {
    console.warn('Turnstile verification failed', JSON.stringify(verify['error-codes'] || []));
    return json({ ok: false, error: 'verification' }, 400);
  }

  // Collect and validate fields
  const d = {};
  for (const [key, max] of Object.entries(LIMITS)) d[key] = (form.get(key) || '').toString().trim().slice(0, max);
  if (!d.name || !EMAIL_RE.test(d.email) || !d.message) return json({ ok: false, error: 'missing-fields' }, 400);

  const rows = [
    ['Name', d.name],
    ['Email', d.email],
    ['Phone', d.phone || '—'],
    ['Service', d.service || '—'],
  ];
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n') + `\n\nProject details:\n${d.message}\n`;
  const html = `
    <div style="font-family:Arial,sans-serif;font-size:15px;color:#111;max-width:560px">
      <h2 style="margin:0 0 16px">New quote request</h2>
      <table cellpadding="6" style="border-collapse:collapse">
        ${rows.map(([k, v]) => `<tr><td style="color:#666;padding-right:16px">${k}</td><td><strong>${escapeHtml(v)}</strong></td></tr>`).join('')}
      </table>
      <p style="color:#666;margin:20px 0 6px">Project details</p>
      <p style="white-space:pre-wrap;margin:0">${escapeHtml(d.message)}</p>
      <p style="color:#999;font-size:12px;margin-top:28px">Sent from the quote form on gcmcgeo.com</p>
    </div>`;

  const email = {
    from: env.MAIL_FROM || 'GCMC Website <website@gcmcgeo.com>',
    to: [env.MAIL_TO || 'jleegcmc@gmail.com'],
    reply_to: d.email,
    subject: `New quote request: ${d.service || 'General'} — ${d.name}`,
    text,
    html,
  };

  if (env.DRY_RUN === '1') {
    console.log('DRY_RUN: would send', JSON.stringify(email));
    return json({ ok: true, dryRun: true });
  }

  if (!env.RESEND_API_KEY) { console.error('RESEND_API_KEY is not set'); return json({ ok: false, error: 'not-configured' }, 500); }
  const sent = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(email),
  }).catch(() => null);

  if (!sent || !sent.ok) {
    // Visible in Cloudflare → Workers & Pages → this project → Functions logs
    console.error('Resend send failed', sent ? sent.status : 'network error', sent ? await sent.text() : '');
    return json({ ok: false, error: 'send-failed' }, 502);
  }
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: 'method-not-allowed' }, 405);
