(() => {
  'use strict';
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const feedback = (target, vars) => {
    if (motion.matches || !window.gsap) return;
    window.gsap.fromTo(target, vars, {
      y: 0, scale: 1, rotation: 0, opacity: 1,
      duration: 0.35, ease: 'power3.out', overwrite: true, clearProps: 'transform,opacity'
    });
  };
  const menuButton = document.querySelector('#menu-toggle');
  const menu = document.querySelector('#mobile-menu');
  const closeMenu = () => {
    menu.hidden = true;
    menu.classList.add('hidden');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Abrir menu');
  };
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menu.hidden = !open;
    menu.classList.toggle('hidden', !open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    if (open) feedback(menu, { y: -8, opacity: 0.5 });
  });
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
  const desktop = window.matchMedia('(min-width: 1024px)');
  desktop.addEventListener('change', event => { if (event.matches) closeMenu(); });

  // This demo stays in memory. No mood choice is stored or transmitted.
  const messages = {
    Excelente: 'Um momento para celebrar. O que fez seu dia brilhar?',
    Bom: 'Que bom. Guarde um pouco desse momento.',
    Neutro: 'Dias tranquilos também fazem parte da sua história.',
    Ruim: 'Dias difíceis também têm espaço aqui.',
    Péssimo: 'Você pode começar só com essa carinha. Sem precisar explicar.'
  };
  const moodButtons = [...document.querySelectorAll('[data-mood]')];
  moodButtons.forEach(button => button.addEventListener('click', () => {
    moodButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.querySelector('.mood-response').textContent = messages[button.dataset.mood];
    feedback(button.querySelector('img'), { y: -8, scale: 1.15, rotation: -10 });
    feedback('.mood-response', { y: 6, opacity: 0.45 });
  }));

  const themeButtons = [...document.querySelectorAll('[data-theme]')];
  themeButtons.forEach(button => button.addEventListener('click', () => {
    const dark = button.dataset.theme === 'dark';
    themeButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const preview = document.querySelector('#theme-screen');
    preview.src = dark ? 'assets/screens/modo-escuro.png' : 'assets/screens/inicio.png';
    preview.alt = dark ? 'Tela inicial no tema escuro' : 'Tela inicial no tema claro';
    document.querySelector('#theme-status').textContent = dark ? 'Prévia do tema escuro.' : 'Prévia do tema claro.';
    feedback(preview, { scale: 0.97, opacity: 0.45 });
  }));

  const gallery = document.querySelector('#gallery');
  const previous = document.querySelector('#gallery-prev');
  const next = document.querySelector('#gallery-next');
  const updateGallery = () => {
    previous.disabled = gallery.scrollLeft < 2;
    next.disabled = gallery.scrollLeft + gallery.clientWidth >= gallery.scrollWidth - 2;
  };
  const moveGallery = direction => {
    const width = gallery.querySelector('figure').getBoundingClientRect().width + 24;
    gallery.scrollBy({ left: width * direction, behavior: motion.matches ? 'instant' : 'smooth' });
  };
  previous.addEventListener('click', () => moveGallery(-1));
  next.addEventListener('click', () => moveGallery(1));
  gallery.addEventListener('scroll', updateGallery, { passive: true });
  gallery.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      moveGallery(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  new ResizeObserver(updateGallery).observe(gallery);
  updateGallery();

  // Progressive enhancement: content and controls do not depend on GSAP.
  if (!window.gsap || !window.ScrollTrigger) return;
  const { gsap, ScrollTrigger } = window;
  gsap.registerPlugin(ScrollTrigger);
  const media = gsap.matchMedia();
  media.add('(prefers-reduced-motion: no-preference)', () => {
    const entrance = gsap.timeline({ defaults: { ease: 'power3.out', duration: 1 } });
    entrance.from('.hero-copy', { y: 24, opacity: 0.35, clearProps: 'all' })
      .from('.hero-phone', { y: 44, rotation: -12, duration: 1.25 }, '<.1')
      .from('.hero-secondary', { y: 34, rotation: 15, duration: 1.25 }, '<.08')
      .from('.hero-face', { scale: 0.75, opacity: 0.4, stagger: 0.12 }, '<.1');
    // One composed opening; gentle movement follows the paired screenshots.
    gsap.to('.hero-stage', {
      y: 35, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 }
    });
    // The faces separate as the diary opens; scrolling carries this composition.
    gsap.utils.toArray('.hero-face').forEach((face, index) => {
      gsap.to(face, {
        y: index ? -30 : 24, rotation: index ? 12 : -14, ease: 'none',
        scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 0.8 }
      });
    });
    gsap.utils.toArray('.feature-panel').forEach(panel => {
      gsap.from(panel.querySelector('.phone'), {
        y: 24, scale: 0.96, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: panel, start: 'top 75%', once: true }
      });
    });
    gsap.from('#aparencia .phone', {
      rotation: -3, y: 20, ease: 'none',
      scrollTrigger: { trigger: '#aparencia', start: 'top bottom', end: 'center center', scrub: 0.8 }
    });
    const finale = gsap.timeline({
      defaults: { ease: 'power3.out' },
      scrollTrigger: { trigger: '.final-cta', start: 'top 75%', once: true }
    });
    finale.from('.cta-faces', { scaleX: 0.8, duration: 0.65 })
      .from('.cta-faces img', {
        x: index => (1 - index) * 32, y: 12, rotation: 0,
        scale: 0.8, stagger: 0.1, duration: 0.7
      }, '<')
      .from('#download-title', { y: 16, opacity: 0.5, duration: 0.65 }, '<.2')
      .from('.final-cta .button-dark', { scale: 0.95, duration: 0.4 }, '<.25');

    // Native controls keep their behavior; motion only acknowledges interaction.
    const cleanups = [];
    const listen = (element, event, callback) => {
      element.addEventListener(event, callback);
      cleanups.push(() => element.removeEventListener(event, callback));
    };
    document.querySelectorAll('.faq-item').forEach(item => {
      listen(item, 'toggle', () => {
        if (item.open) feedback(item.querySelector('p'), { y: -5, opacity: 0.4 });
      });
    });
    const hover = window.matchMedia('(hover: hover) and (pointer: fine)');
    document.querySelectorAll('.mood-choice').forEach(button => {
      listen(button, 'pointerenter', () => {
        if (hover.matches) feedback(button.querySelector('img'), { y: -5, rotation: -8, scale: 1.08 });
      });
    });
    return () => cleanups.forEach(cleanup => cleanup());
  });
  document.fonts.ready.then(() => ScrollTrigger.refresh());
  window.addEventListener('load', () => ScrollTrigger.refresh(), { once: true });
})();
