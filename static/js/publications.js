(() => {
  const controls = document.querySelector('[data-publication-filters]');
  if (!controls) return;
  const buttons = [...controls.querySelectorAll('button[data-area]')];
  const papers = [...document.querySelectorAll('#publication-list .publication')];
  const status = controls.querySelector('[role="status"]');
  function select(area, updateURL = false) {
    if (!buttons.some(button => button.dataset.area === area)) area = 'all';
    let count = 0;
    papers.forEach(paper => {
      const matches = area === 'all' || paper.dataset.areas.split(' ').includes(area);
      paper.hidden = !matches;
      if (matches) count++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.area === area)));
    status.textContent = `Showing ${count} of ${papers.length} publications`;
    if (updateURL) {
      const url = new URL(window.location.href);
      if (area === 'all') url.searchParams.delete('area');
      else url.searchParams.set('area', area);
      history.pushState(null, '', url);
    }
  }
  const fromURL = () => select(new URLSearchParams(location.search).get('area') || 'all');
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.area, true)));
  window.addEventListener('popstate', fromURL);
  fromURL();
  controls.hidden = false;
})();
