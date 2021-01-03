window.addEventListener('load', () => {
    const cookieNoticeShown = localStorage.getItem('cookieNotice');
    if (cookieNoticeShown) { return; }

    const cookieNotice = document.createElement('div');
    cookieNotice.innerText = "This website uses cookies to store information about the games you play.";
    cookieNotice.setAttribute('id', 'cookie-notice');
    const closeButton = document.createElement('span');
    closeButton.setAttribute('id', 'close-button');
    closeButton.innerText = 'X';
    cookieNotice.appendChild(closeButton);
    document.body.appendChild(cookieNotice);
    cookieNotice.addEventListener('click', () => {
        localStorage.setItem('cookieNotice', "1");
        document.body.removeChild(cookieNotice);
    });
});
