(() => {
  'use strict';

  const originalHeader = document.querySelector('header.site-header');
  const originalMobileNav = document.querySelector('#mobile-nav');
  if (!originalHeader || !originalMobileNav) return;

  const header = originalHeader.cloneNode(true);
  const mobileNav = originalMobileNav.cloneNode(true);
  originalHeader.replaceWith(header);
  originalMobileNav.replaceWith(mobileNav);
  const toggle = header.querySelector('.menu-toggle');
  if (!toggle) return;

  const desktop = window.matchMedia('(min-width: 1080px)');
  const focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  let lastFocused = null;

  header.querySelector('.brand')?.setAttribute('href', '/');
  document.querySelectorAll('.mega-toggle').forEach((trigger) => {
    trigger.setAttribute('aria-expanded', 'false');
    const panel = trigger.nextElementSibling;
    if (panel && !panel.id) panel.id = `mega-${trigger.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-')}`;
    if (panel?.id) trigger.setAttribute('aria-controls', panel.id);
  });

  const normalisePath = (value) => {
    const path = value.replace(/index\.html$/, '').replace(/\.html$/, '').replace(/\/$/, '');
    return path || '/';
  };
  const currentPath = normalisePath(window.location.pathname);
  document.querySelectorAll('.site-header a[href], .mobile-nav a[href]').forEach((link) => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || /^(?:mailto:|tel:|https?:)/i.test(href)) return;
    if (normalisePath(new URL(href, window.location.href).pathname) === currentPath) link.setAttribute('aria-current', 'page');
  });

  const setMenu = (open, { restoreFocus = false } = {}) => {
    if (desktop.matches) open = false;
    mobileNav.classList.toggle('open', open);
    mobileNav.inert = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('site-menu-open', open);
    if (open) {
      lastFocused = document.activeElement;
      requestAnimationFrame(() => mobileNav.querySelector(focusableSelector)?.focus());
    } else if (restoreFocus) {
      (lastFocused instanceof HTMLElement ? lastFocused : toggle).focus();
    }
  };

  const closeMegaMenus = (except = null) => {
    header.querySelectorAll('.mega-menu').forEach((menu) => {
      if (menu === except) return;
      menu.classList.remove('is-open');
      menu.querySelector('.mega-toggle')?.setAttribute('aria-expanded', 'false');
    });
  };

  toggle.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();
    setMenu(toggle.getAttribute('aria-expanded') !== 'true');
  }, true);

  mobileNav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false);
  });

  header.querySelectorAll('button.mega-toggle').forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      const menu = button.closest('.mega-menu');
      const open = !menu.classList.contains('is-open');
      closeMegaMenus(menu);
      menu.classList.toggle('is-open', open);
      button.setAttribute('aria-expanded', String(open));
    });
  });

  header.querySelectorAll('.mega-menu').forEach((menu) => {
    const trigger = menu.querySelector('.mega-toggle');
    menu.addEventListener('focusin', () => {
      menu.classList.remove('is-closed');
      closeMegaMenus(menu);
      menu.classList.add('is-open');
      trigger?.setAttribute('aria-expanded', 'true');
    });
    menu.addEventListener('focusout', () => {
      requestAnimationFrame(() => {
        if (menu.contains(document.activeElement)) return;
        menu.classList.remove('is-open');
        trigger?.setAttribute('aria-expanded', 'false');
      });
    });
    menu.addEventListener('mouseleave', () => menu.classList.remove('is-closed'));
  });

  document.addEventListener('click', (event) => {
    if (!header.contains(event.target)) closeMegaMenus();
    if (!header.contains(event.target) && !mobileNav.contains(event.target)) setMenu(false);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      const wasOpen = mobileNav.classList.contains('open');
      const activeMegaMenu = document.activeElement?.closest?.('.mega-menu');
      if (activeMegaMenu) {
        activeMegaMenu.querySelector('.mega-toggle')?.focus();
        activeMegaMenu.classList.add('is-closed');
      }
      closeMegaMenus();
      setMenu(false, { restoreFocus: wasOpen });
      return;
    }
    if (event.key !== 'Tab' || !mobileNav.classList.contains('open')) return;
    const items = [...mobileNav.querySelectorAll(focusableSelector)].filter((item) => item.offsetParent !== null);
    if (!items.length) return;
    const first = items[0];
    const last = items.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  desktop.addEventListener('change', () => {
    closeMegaMenus();
    setMenu(false);
  });

  const syncHeaderHeight = () => {
    document.documentElement.style.setProperty('--site-header-height', `${Math.ceil(header.getBoundingClientRect().height)}px`);
  };
  syncHeaderHeight();
  new ResizeObserver(syncHeaderHeight).observe(header);
  setMenu(false);
})();
