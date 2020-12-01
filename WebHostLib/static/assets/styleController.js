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

window.addEventListener('load', () => {
  adjustFooterHeight();
  window.addEventListener('resize', adjustFooterHeight);
});
