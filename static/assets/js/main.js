/**
 * AgriCulture Expert System - Mobile Navigation & UI Enhancements
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Navigation Toggle Handler
  const toggleBtn = document.querySelector('.mobile-nav-toggle');
  const navmenu = document.querySelector('#navmenu') || document.querySelector('.navmenu');

  if (toggleBtn && navmenu) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      navmenu.classList.toggle('mobile-nav-active');
      toggleBtn.classList.toggle('bi-list');
      toggleBtn.classList.toggle('bi-x');
    });

    // Close when tapping anywhere outside the mobile drawer
    document.addEventListener('click', (e) => {
      if (!navmenu.contains(e.target) && !toggleBtn.contains(e.target) && navmenu.classList.contains('mobile-nav-active')) {
        navmenu.classList.remove('mobile-nav-active');
        toggleBtn.classList.add('bi-list');
        toggleBtn.classList.remove('bi-x');
      }
    });

    // Close when clicking any nav link
    navmenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navmenu.classList.remove('mobile-nav-active');
        toggleBtn.classList.add('bi-list');
        toggleBtn.classList.remove('bi-x');
      });
    });
  }
});

