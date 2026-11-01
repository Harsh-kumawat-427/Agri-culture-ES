/**
 * AgriCulture Expert System - Mobile Navigation & UI Enhancements
 * Implements accessible, high-performance top-right dropdown navigation.
 */

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.querySelector('.mobile-nav-toggle');
  const navmenu = document.querySelector('#navmenu') || document.querySelector('.navmenu');

  if (toggleBtn && navmenu) {
    // 1. Ensure backdrop element exists in the DOM
    let backdrop = document.querySelector('.mobile-nav-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'mobile-nav-backdrop';
      backdrop.setAttribute('aria-hidden', 'true');
      document.body.appendChild(backdrop);
    }

    // 2. Set accessibility attributes
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.setAttribute('aria-label', 'Toggle Navigation Menu');
    toggleBtn.setAttribute('aria-controls', 'navmenu');
    toggleBtn.setAttribute('role', 'button');
    toggleBtn.setAttribute('tabindex', '0');

    // 3. Inject header inside navmenu if not present
    if (!navmenu.querySelector('.navmenu-header')) {
      const headerDiv = document.createElement('div');
      headerDiv.className = 'navmenu-header d-lg-none';
      headerDiv.innerHTML = `
        <span class="navmenu-title"><i class="bi bi-flower1"></i> Quick Menu</span>
        <button type="button" class="btn-close-nav" aria-label="Close navigation" title="Close"><i class="bi bi-x-lg"></i></button>
      `;
      navmenu.insertBefore(headerDiv, navmenu.firstChild);
    }

    // 4. Inject footer credits inside navmenu if not present
    if (!navmenu.querySelector('.navmenu-footer')) {
      const footerDiv = document.createElement('div');
      footerDiv.className = 'navmenu-footer d-lg-none';
      footerDiv.innerHTML = `
        <div class="fw-bold text-success mb-0">AgriCulture AI Advisor</div>
        <div>Harsh Kumawat · Harshul Bhanwar · Hariom Patidar</div>
        <div class="text-muted" style="font-size: 10.5px;">Medi-Caps University</div>
      `;
      navmenu.appendChild(footerDiv);
    }

    const openMenu = () => {
      navmenu.classList.add('mobile-nav-active');
      backdrop.classList.add('active');
      toggleBtn.classList.remove('bi-list');
      toggleBtn.classList.add('bi-x');
      toggleBtn.setAttribute('aria-expanded', 'true');
      document.body.classList.add('mobile-nav-open');
    };

    const closeMenu = () => {
      navmenu.classList.remove('mobile-nav-active');
      backdrop.classList.remove('active');
      toggleBtn.classList.add('bi-list');
      toggleBtn.classList.remove('bi-x');
      toggleBtn.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('mobile-nav-open');
    };

    // Toggle button handler
    toggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (navmenu.classList.contains('mobile-nav-active')) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    // Enter/Space keyboard accessibility for toggle button
    toggleBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleBtn.click();
      }
    });

    // Internal close button handler
    navmenu.addEventListener('click', (e) => {
      const closeBtn = e.target.closest('.btn-close-nav');
      if (closeBtn) {
        e.preventDefault();
        e.stopPropagation();
        closeMenu();
        toggleBtn.focus();
      }
    });

    // Backdrop click dismisses menu
    backdrop.addEventListener('click', (e) => {
      e.preventDefault();
      closeMenu();
    });

    // Navigation links handling:
    // For hash links, smooth scroll and close.
    // For standard page links, allow browser to navigate without cancelling the click event!
    navmenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
          e.preventDefault();
          closeMenu();
          const target = document.querySelector(href);
          if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
          }
        } else {
          // Standard page navigation - do not prevent default, do not hide synchronously
          setTimeout(() => {
            closeMenu();
          }, 250);
        }
      });
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navmenu.classList.contains('mobile-nav-active')) {
        closeMenu();
        toggleBtn.focus();
      }
    });
  }
});
