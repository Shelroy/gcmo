/* GCMC — site interactions */
(() => {
  const doc = document.documentElement;
  doc.classList.remove('no-js');
  doc.classList.add('js');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  /* ---------- Header: solid after scrolling, hide on scroll down ---------- */
  const header = $('.header');
  let lastY = window.scrollY;
  const onScrollHeader = () => {
    if (!header) return;
    const y = window.scrollY;
    header.classList.toggle('is-solid', y > 40);
    const goingDown = y > lastY && y > 400;
    header.classList.toggle('is-hidden', goingDown && !document.body.classList.contains('menu-open'));
    lastY = y;
  };
  onScrollHeader();
  window.addEventListener('scroll', onScrollHeader, { passive: true });

  /* ---------- Mobile menu ---------- */
  const menuBtn = $('.menu-btn');
  const mobileMenu = $('#mobile-menu');
  const setMenu = (open) => {
    document.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    mobileMenu.setAttribute('aria-hidden', String(!open));
    if (open) { header.classList.remove('is-hidden'); $('a', mobileMenu).focus({ preventScroll: true }); }
  };
  menuBtn?.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && document.body.classList.contains('menu-open')) { setMenu(false); menuBtn.focus(); } });
  $$('a', mobileMenu || document.createElement('div')).forEach((a) => a.addEventListener('click', () => setMenu(false)));

  /* ---------- Split headings into words ---------- */
  $$('[data-split]').forEach((el) => {
    let i = 0;
    const walk = (node) => {
      [...node.childNodes].forEach((child) => {
        if (child.nodeType === 3) {
          const frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            const outer = document.createElement('span');
            outer.className = 'split-word';
            const inner = document.createElement('span');
            inner.style.setProperty('--i', i++);
            inner.textContent = part;
            outer.appendChild(inner);
            frag.appendChild(outer);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === 1 && child.tagName !== 'BR') {
          walk(child);
        }
      });
    };
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    walk(el);
    $$('.split-word', el).forEach((w) => w.setAttribute('aria-hidden', 'true'));
  });

  /* ---------- Reveal on scroll ---------- */
  const revealEls = $$('[data-reveal], [data-split]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-in'));
  }
  // Headline in the hero animates straight away
  $$('.hero [data-split], .page-hero [data-split]').forEach((el) => requestAnimationFrame(() => el.classList.add('is-in')));

  /* ---------- Hero slideshow ---------- */
  const hero = $('.hero');
  if (hero) {
    const slides = $$('.hero__slide', hero);
    const dots = $$('.hero__progress button', hero);
    const caption = $('.hero__caption', hero);
    const SLIDE_MS = 7000;
    hero.style.setProperty('--slide-ms', SLIDE_MS + 'ms');
    let current = 0; let timer;
    let paused = reduceMotion;
    const pauseBtn = $('.hero__pause', hero);
    const setPaused = (p) => {
      paused = p;
      hero.classList.toggle('is-paused', p);
      pauseBtn?.setAttribute('aria-pressed', String(p));
      pauseBtn?.setAttribute('aria-label', p ? 'Play slideshow' : 'Pause slideshow');
    };
    pauseBtn?.addEventListener('click', () => {
      setPaused(!paused);
      if (paused) clearTimeout(timer); else show(current + 1);
    });
    setPaused(paused);
    const show = (n) => {
      current = (n + slides.length) % slides.length;
      slides.forEach((s, i) => {
        s.classList.toggle('is-active', i === current);
        const img = $('img', s);
        if (i === current && img.loading === 'lazy') img.loading = 'eager';
      });
      dots.forEach((d, i) => {
        d.classList.remove('is-active', 'is-done');
        void d.offsetWidth; // restart the progress animation
        if (i < current) d.classList.add('is-done');
        if (i === current) d.classList.add('is-active');
        d.setAttribute('aria-current', i === current ? 'true' : 'false');
      });
      if (caption) caption.textContent = slides[current].dataset.caption || '';
      clearTimeout(timer);
      if (!paused) timer = setTimeout(() => show(current + 1), SLIDE_MS);
    };
    dots.forEach((d, i) => d.addEventListener('click', () => show(i)));
    document.addEventListener('visibilitychange', () => { if (document.hidden) clearTimeout(timer); else if (!paused) show(current); });
    show(0);
  }

  /* ---------- Parallax ---------- */
  const parallaxEls = $$('[data-parallax]');
  if (parallaxEls.length && !reduceMotion) {
    let ticking = false;
    const update = () => {
      const vh = window.innerHeight;
      parallaxEls.forEach((el) => {
        const r = el.parentElement.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) return;
        const speed = parseFloat(el.dataset.parallax) || 0.15;
        const offset = (r.top + r.height / 2 - vh / 2) * -speed;
        el.style.transform = `translate3d(0, ${offset.toFixed(1)}px, 0)`;
      });
      ticking = false;
    };
    window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  /* ---------- Count-up numbers ---------- */
  const counters = $$('[data-count]');
  if (counters.length) {
    const run = (el) => {
      const target = parseInt(el.dataset.count, 10);
      if (reduceMotion) { el.textContent = target; return; }
      const start = performance.now(); const dur = 1600;
      const tick = (now) => {
        const p = Math.min((now - start) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const cio = new IntersectionObserver((entries) => entries.forEach((e) => { if (e.isIntersecting) { run(e.target); cio.unobserve(e.target); } }), { threshold: 0.6 });
    counters.forEach((c) => cio.observe(c));
  }

  /* ---------- Horizontal work rail ---------- */
  const railSection = $('.rail-section');
  if (railSection) {
    const rail = $('.rail', railSection);
    const sticky = $('.rail-sticky', railSection);
    const bar = $('.rail-progress span', railSection);
    const mq = window.matchMedia('(min-width: 1000px) and (prefers-reduced-motion: no-preference)');
    let distance = 0;
    const measure = () => {
      if (mq.matches) {
        railSection.classList.add('is-pinned');
        rail.style.transform = '';
        distance = Math.max(0, rail.scrollWidth - window.innerWidth);
        railSection.style.height = `${window.innerHeight + distance}px`;
      } else {
        railSection.classList.remove('is-pinned');
        railSection.style.height = '';
        rail.style.transform = '';
      }
      onRail();
    };
    const onRail = () => {
      if (!mq.matches) {
        const max = rail.scrollWidth - rail.clientWidth;
        if (bar) bar.style.transform = `scaleX(${max > 0 ? rail.scrollLeft / max : 0})`;
        return;
      }
      const top = railSection.getBoundingClientRect().top;
      const p = Math.min(Math.max(-top / (distance || 1), 0), 1);
      rail.style.transform = `translate3d(${-p * distance}px, 0, 0)`;
      if (bar) bar.style.transform = `scaleX(${p})`;
    };
    window.addEventListener('scroll', () => requestAnimationFrame(onRail), { passive: true });
    rail.addEventListener('scroll', onRail, { passive: true });
    window.addEventListener('resize', measure);
    window.addEventListener('load', measure);
    measure();
    $$('.rail-controls button', railSection).forEach((b) => b.addEventListener('click', () => {
      const step = rail.clientWidth * 0.8 * (b.dataset.dir === 'prev' ? -1 : 1);
      rail.scrollBy({ left: step, behavior: reduceMotion ? 'auto' : 'smooth' });
    }));
    void sticky;
  }

  /* ---------- Video ---------- */
  $$('.video-block').forEach((block) => {
    const video = $('.video-block__main', block);
    const loop = $('.video-block__loop', block);
    const btn = $('.play-btn', block);
    if (loop && !reduceMotion && 'IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => {
        if (block.classList.contains('is-playing')) return;
        if (e.isIntersecting) loop.play().catch(() => {}); else loop.pause();
      }, { threshold: 0.25 }).observe(block);
    }
    btn?.addEventListener('click', () => {
      loop?.pause();
      block.classList.add('is-playing');
      video.setAttribute('controls', '');
      video.play();
      video.focus();
    });
  });

  /* ---------- Services sub-nav highlight ---------- */
  const subLinks = $$('.subnav a');
  if (subLinks.length) {
    const map = new Map(subLinks.map((a) => [a.getAttribute('href').slice(1), a]));
    const sio = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          subLinks.forEach((a) => a.classList.remove('is-active'));
          const link = map.get(e.target.id);
          if (link) { link.classList.add('is-active'); link.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' }); }
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) sio.observe(s); });
  }

  /* ---------- FAQ: smooth open/close ---------- */
  $$('.faq details').forEach((d) => {
    const summary = $('summary', d);
    const body = $('.faq__body', d);
    summary.addEventListener('click', (e) => {
      if (reduceMotion) return;
      e.preventDefault();
      if (d.open) {
        const anim = body.animate([{ height: body.offsetHeight + 'px' }, { height: '0px' }], { duration: 380, easing: 'cubic-bezier(.65,0,.35,1)' });
        anim.onfinish = () => { d.open = false; };
      } else {
        d.open = true;
        body.animate([{ height: '0px' }, { height: body.offsetHeight + 'px' }], { duration: 450, easing: 'cubic-bezier(.22,.8,.2,1)' });
      }
    });
  });

  /* ---------- Projects: filter + lightbox ---------- */
  const grid = $('.masonry');
  if (grid) {
    const tiles = $$('.tile', grid);
    const buttons = $$('.filter-btn');
    buttons.forEach((btn) => btn.addEventListener('click', () => {
      const f = btn.dataset.filter;
      buttons.forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
      tiles.forEach((t, i) => {
        const show = f === 'all' || t.dataset.cat === f;
        t.classList.toggle('is-hidden', !show);
        if (show && !reduceMotion) {
          t.classList.add('is-entering');
          setTimeout(() => t.classList.remove('is-entering'), 30 + Math.min(i, 12) * 35);
        }
      });
      const url = new URL(location.href);
      if (f === 'all') url.searchParams.delete('type'); else url.searchParams.set('type', f);
      history.replaceState(null, '', url);
    }));
    const initial = new URLSearchParams(location.search).get('type');
    if (initial) buttons.find((b) => b.dataset.filter === initial)?.click();

    const lb = $('.lightbox');
    const lbImg = $('.lightbox__stage img', lb);
    const lbCap = $('.lightbox__cap', lb);
    const lbCount = $('.lightbox__count', lb);
    let list = []; let idx = 0; let lastFocus;
    const render = () => {
      const t = list[idx];
      const btn = $('button', t);
      lbImg.classList.add('is-swapping');
      const src = btn.dataset.full;
      const pre = new Image();
      pre.onload = pre.onerror = () => {
        lbImg.src = src; lbImg.alt = $('img', t).alt;
        requestAnimationFrame(() => lbImg.classList.remove('is-swapping'));
      };
      pre.src = src;
      lbCap.textContent = $('img', t).alt;
      lbCount.textContent = `${idx + 1} / ${list.length}`;
    };
    const open = (tile) => {
      list = tiles.filter((t) => !t.classList.contains('is-hidden'));
      idx = list.indexOf(tile);
      lastFocus = document.activeElement;
      lb.classList.add('is-open');
      lb.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      render();
      $('.lb-close', lb).focus();
    };
    const close = () => {
      lb.classList.remove('is-open');
      lb.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      lastFocus?.focus();
    };
    const step = (n) => { idx = (idx + n + list.length) % list.length; render(); };
    tiles.forEach((t) => $('button', t).addEventListener('click', () => open(t)));
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', () => step(-1));
    $('.lb-next', lb).addEventListener('click', () => step(1));
    lb.addEventListener('click', (e) => { if (e.target === lb || e.target.classList.contains('lightbox__stage')) close(); });
    document.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'Tab') { // keep focus inside the lightbox
        const f = $$('button', lb); const first = f[0]; const last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    let sx = 0;
    lb.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (e) => { const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); });
  }

  /* ---------- Contact form: validate, then send to /api/contact ---------- */
  const form = $('#quote-form');
  if (form) {
    const status = $('.form__status', form);
    const submitBtn = $('button[type="submit"]', form);
    const setStatus = (msg, type) => { status.className = `form__status is-${type}`; status.innerHTML = msg; };
    const mailtoHref = (data) => {
      const subject = `Project enquiry: ${data.get('service') || 'General'} — ${data.get('name')}`;
      const body = [`Name: ${data.get('name')}`, `Email: ${data.get('email')}`, `Phone: ${data.get('phone') || '—'}`, `Service: ${data.get('service') || '—'}`, '', data.get('message')].join('\n');
      return `mailto:${form.dataset.to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    };
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      let ok = true;
      $$('[required]', form).forEach((input) => {
        const field = input.closest('.field');
        const valid = input.type === 'email' ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()) : input.value.trim() !== '';
        field.classList.toggle('has-error', !valid);
        input.setAttribute('aria-invalid', String(!valid));
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;
      const data = new FormData(form);
      if (window.turnstile && !data.get('cf-turnstile-response')) {
        setStatus('Please complete the quick security check above, then send again.', 'error');
        return;
      }
      submitBtn.classList.add('is-loading');
      $('.btn__label', submitBtn).textContent = 'Sending…';
      try {
        const res = await fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
        const out = await res.json().catch(() => ({}));
        if (res.ok && out.ok) {
          form.classList.add('is-sent');
          setStatus(`<strong>Thank you, ${data.get('name').split(' ')[0].replace(/[<>&]/g, '')}!</strong> Your enquiry is on its way. We'll be in touch soon.`, 'success');
          status.focus?.();
          return;
        }
        if (out.error === 'verification') {
          setStatus('The security check didn\'t go through. Please try it again.', 'error');
          window.turnstile?.reset();
        } else {
          setStatus(`Sorry, your message couldn't be sent. Please <a href="${mailtoHref(data)}">email it to us instead</a> or call <a href="tel:${document.querySelector('a[href^="tel:"]').getAttribute('href').slice(4)}">us</a>.`, 'error');
        }
      } catch {
        setStatus(`Sorry, your message couldn't be sent. Please <a href="${mailtoHref(data)}">email it to us instead</a>.`, 'error');
      } finally {
        submitBtn.classList.remove('is-loading');
        $('.btn__label', submitBtn).textContent = 'Send enquiry';
      }
    });
    $$('input, textarea', form).forEach((i) => i.addEventListener('input', () => i.closest('.field').classList.remove('has-error')));
    // Preselect the service when arriving from a service page (/contact?service=...)
    const pre = new URLSearchParams(location.search).get('service');
    const opt = pre && $(`#f-service option[data-id="${CSS.escape(pre)}"]`);
    if (opt) opt.selected = true;
  }

  /* ---------- Before / after slider ---------- */
  $$('.compare').forEach((cmp) => {
    const range = $('.compare__range', cmp);
    const set = (v) => cmp.style.setProperty('--pos', `${v}%`);
    range.addEventListener('input', () => { cmp.classList.remove('is-hinting'); set(range.value); });
    if (reduceMotion || !('IntersectionObserver' in window)) return;
    // A one-time nudge so visitors see it can be dragged
    const io = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return;
      io.disconnect();
      cmp.classList.add('is-hinting');
      setTimeout(() => set(72), 400);
      setTimeout(() => set(30), 1500);
      setTimeout(() => { set(50); range.value = 50; }, 2600);
      setTimeout(() => cmp.classList.remove('is-hinting'), 3900);
    }, { threshold: 0.6 });
    io.observe(cmp);
  });

  /* ---------- Magnetic buttons and tilting images (mouse only) ---------- */
  if (!reduceMotion && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    $$('[data-magnetic]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.22;
        const y = (e.clientY - r.top - r.height / 2) * 0.32;
        el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
    $$('[data-tilt]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = `perspective(900px) rotateY(${(px * 6).toFixed(2)}deg) rotateX(${(-py * 6).toFixed(2)}deg)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  }

  /* ---------- Sticky mobile contact bar ---------- */
  const bar = $('.mobile-bar');
  if (bar) {
    const onBar = () => bar.classList.toggle('is-visible', window.scrollY > window.innerHeight * 0.6);
    onBar();
    window.addEventListener('scroll', onBar, { passive: true });
  }

  /* ---------- Footer year ---------- */
  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
