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

  // Multi-select dropdowns
  (() => {
    const dropdowns = document.querySelectorAll('.ms-dropdown');
    if (!dropdowns.length) return;

    dropdowns.forEach(dd => {
      const btn = dd.querySelector('.ms-dropdown-btn');
      const label = dd.querySelector('.ms-dropdown-label');
      const hidden = dd.querySelector('.ms-dropdown-hidden');
      const checks = dd.querySelectorAll('.ms-option input[type="checkbox"]');
      const placeholder = label.dataset.placeholder || 'Select';

      const update = () => {
        const selected = Array.from(checks).filter(c => c.checked).map(c => c.value);
        hidden.value = selected.join(', ');
        if (selected.length === 0) {
          label.textContent = placeholder;
          label.classList.remove('has-value');
        } else if (selected.length === 1) {
          label.textContent = selected[0];
          label.classList.add('has-value');
        } else {
          label.textContent = selected.length + ' selected';
          label.classList.add('has-value');
        }
      };

      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        dd.classList.toggle('open');
      });
      checks.forEach(c => c.addEventListener('change', update));
    });

    document.addEventListener('click', (e) => {
      document.querySelectorAll('.ms-dropdown.open').forEach(dd => {
        if (!dd.contains(e.target)) dd.classList.remove('open');
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.ms-dropdown.open').forEach(dd => dd.classList.remove('open'));
      }
    });
  })();
