window.addEventListener('load', () => {
    const cookieNoticeShown = localStorage.getItem('cookieNotice');
    if (cookieNoticeShown) { return; }

    const cookieNotice = document.createElement('div');
    cookieNotice.innerText = "This website uses cookies to store information about the games you play.";
    cookieNotice.style.position = "fixed";
    cookieNotice.style.bottom = "0";
    cookieNotice.style.left = "0";
    cookieNotice.style.width = "100%";
    cookieNotice.style.lineHeight = "40px";
    cookieNotice.style.backgroundColor = "#c7cda5";
    cookieNotice.style.textAlign = "center";
    cookieNotice.style.cursor = "pointer";
    document.body.appendChild(cookieNotice);
    cookieNotice.addEventListener('click', () => {
        localStorage.setItem('cookieNotice', "1");
        document.body.removeChild(cookieNotice);
    });
});
