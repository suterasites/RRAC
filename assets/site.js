  document.getElementById('year').textContent = new Date().getFullYear();
  const navToggle = document.getElementById('navToggle');
  const mobileNav = document.getElementById('mobileNav');
  navToggle?.addEventListener('click', () => mobileNav.classList.toggle('hidden'));

  // Mega menu
  (() => {
    const wraps = document.querySelectorAll('.mega-wrap');
    const headerNav = document.querySelector('.header-nav');
    let activePanel = null;
    let activeWrap = null;
    let closeTimer = null;

    const closeAll = () => {
      if (activePanel) activePanel.classList.remove('active');
      if (activeWrap) {
        activeWrap.classList.remove('open');
        const trig = activeWrap.querySelector('.mega-trigger');
        if (trig) trig.setAttribute('aria-expanded', 'false');
      }
      headerNav?.classList.remove('menu-active');
      activePanel = null;
      activeWrap = null;
    };

    wraps.forEach(wrap => {
      const id = wrap.dataset.mega;
      const panel = document.getElementById('mega-' + id);
      if (!panel) return;
      const trigger = wrap.querySelector('.mega-trigger');

      const open = () => {
        clearTimeout(closeTimer);
        if (activePanel && activePanel !== panel) closeAll();
        panel.classList.add('active');
        wrap.classList.add('open');
        headerNav?.classList.add('menu-active');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
        activePanel = panel;
        activeWrap = wrap;
      };
      const deferClose = () => {
        clearTimeout(closeTimer);
        closeTimer = setTimeout(closeAll, 180);
      };

      wrap.addEventListener('mouseenter', open);
      wrap.addEventListener('mouseleave', deferClose);
      panel.addEventListener('mouseenter', () => clearTimeout(closeTimer));
      panel.addEventListener('mouseleave', deferClose);

      trigger?.addEventListener('click', (e) => {
        if (window.matchMedia('(hover: none)').matches) {
          e.preventDefault();
          if (activePanel === panel) closeAll(); else open();
        }
      });
    });

    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeAll(); });
  })();
