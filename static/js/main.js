/**
 * Signia Home Care — Main JavaScript
 * Handles: mobile nav, flash dismiss, smooth scroll, scroll animations
 */

(function () {
  'use strict';

  // ---------------------------------------------------------------
  // Mobile Navigation Toggle
  // ---------------------------------------------------------------
  const navToggle   = document.getElementById('navToggle');
  const primaryNav  = document.getElementById('primaryNav');
  const body        = document.body;

  if (navToggle && primaryNav) {
    navToggle.addEventListener('click', function () {
      const isOpen = primaryNav.classList.toggle('is-open');
      navToggle.classList.toggle('is-active', isOpen);
      navToggle.setAttribute('aria-expanded', String(isOpen));
      body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close nav on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && primaryNav.classList.contains('is-open')) {
        primaryNav.classList.remove('is-open');
        navToggle.classList.remove('is-active');
        navToggle.setAttribute('aria-expanded', 'false');
        body.style.overflow = '';
        navToggle.focus();
      }
    });

    // Close nav when a link is clicked (mobile)
    primaryNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth < 1024) {
          primaryNav.classList.remove('is-open');
          navToggle.classList.remove('is-active');
          navToggle.setAttribute('aria-expanded', 'false');
          body.style.overflow = '';
        }
      });
    });
  }

  // ---------------------------------------------------------------
  // Flash Message Dismiss
  // ---------------------------------------------------------------
  document.querySelectorAll('.flash__close').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const flash = btn.closest('.flash');
      if (flash) {
        flash.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        flash.style.opacity = '0';
        flash.style.transform = 'translateX(10px)';
        setTimeout(function () { flash.remove(); }, 300);
      }
    });
  });

  // Auto-dismiss flash messages after 6 seconds
  setTimeout(function () {
    document.querySelectorAll('.flash').forEach(function (flash) {
      flash.style.transition = 'opacity 0.5s ease';
      flash.style.opacity = '0';
      setTimeout(function () { flash.remove(); }, 500);
    });
  }, 6000);

  // ---------------------------------------------------------------
  // Scroll-triggered Animations (IntersectionObserver)
  // ---------------------------------------------------------------
  if ('IntersectionObserver' in window) {
    const animTargets = document.querySelectorAll(
      '.card, .feature-item, .service-mini-card, .value-card, .stat-item, .referral-step'
    );

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    animTargets.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      observer.observe(el);
    });
  }

  // ---------------------------------------------------------------
  // Sticky Header Shadow
  // ---------------------------------------------------------------
  const siteHeader = document.querySelector('.site-header');
  if (siteHeader) {
    window.addEventListener('scroll', function () {
      siteHeader.style.boxShadow = window.scrollY > 10
        ? '0 2px 20px rgba(0,0,0,0.10)'
        : '0 1px 2px rgba(0,0,0,0.05)';
    }, { passive: true });
  }

  // ---------------------------------------------------------------
  // Form: Basic Client-Side Validation Feedback
  // ---------------------------------------------------------------
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      let valid = true;
      form.querySelectorAll('[required]').forEach(function (field) {
        if (!field.value.trim()) {
          field.style.borderColor = 'var(--color-error)';
          valid = false;
        } else {
          field.style.borderColor = '';
        }
      });
      if (!valid) {
        e.preventDefault();
        const firstInvalid = form.querySelector('[required]:placeholder-shown, [required][value=""]');
        if (firstInvalid) firstInvalid.focus();
      }
    });

    // Clear error styling on input
    form.querySelectorAll('input, select, textarea').forEach(function (field) {
      field.addEventListener('input', function () {
        field.style.borderColor = '';
      });
    });
  });

  // ---------------------------------------------------------------
  // Smooth scroll for anchor links
  // ---------------------------------------------------------------
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
      }
    });
  });

})();
