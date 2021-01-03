const adjustFooterHeight = () => {
  // If there is no footer on this page, do nothing
  const footer = document.getElementById('island-footer');
  if (!footer) { return; }

  // If the body is taller than the window, also do nothing
  if (document.body.offsetHeight > window.innerHeight) {
    footer.style.marginTop = '0';
    return;
  }

  // Add a margin-top to the footer to position it at the bottom of the screen
  const sibling = footer.previousElementSibling;
  const margin = (window.innerHeight - sibling.offsetTop - sibling.offsetHeight - footer.offsetHeight);
  if (margin < 1) {
    footer.style.marginTop = '0';
    return;
  }
  footer.style.marginTop = `${margin}px`;
};

const adjustHeaderWidth = () => {
  // If there is no header, do nothing
  const header = document.getElementById('base-header');
  if (!header) { return; }

  const tempDiv = document.createElement('div');
  tempDiv.style.width = '100px';
  tempDiv.style.height = '100px';
  tempDiv.style.overflow = 'scroll';
  tempDiv.style.position = 'absolute';
  tempDiv.style.top = '-500px';
  document.body.appendChild(tempDiv);
  const scrollbarWidth = tempDiv.offsetWidth - tempDiv.clientWidth;
  document.body.removeChild(tempDiv);

  const documentRoot = document.compatMode === 'BackCompat' ? document.body : document.documentElement;
  const margin = (documentRoot.scrollHeight > documentRoot.clientHeight) ? 0-scrollbarWidth : 0;
  document.getElementById('base-header-right').style.marginRight = `${margin}px`;
};

window.addEventListener('load', () => {
  window.addEventListener('resize', adjustFooterHeight);
  window.addEventListener('resize', adjustHeaderWidth);
  adjustFooterHeight();
  adjustHeaderWidth();
});
