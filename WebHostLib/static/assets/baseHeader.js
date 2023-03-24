window.addEventListener('load', () => {
  const menuButton = document.getElementById('base-header-mobile-menu-button');
  const mobileMenu = document.getElementById('base-header-mobile-menu');

  menuButton.addEventListener('click', (evt) => {
    evt.preventDefault();

    if (!mobileMenu.style.display || mobileMenu.style.display === 'none') {
      return mobileMenu.style.display = 'flex';
    }

    mobileMenu.style.display = 'none';
  });

  window.addEventListener('resize', () => {
    mobileMenu.style.display = 'none';
  });
});
