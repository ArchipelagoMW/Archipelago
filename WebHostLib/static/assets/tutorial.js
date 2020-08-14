window.addEventListener('load', () => {
    const headers = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    const scrollTargetIndex = window.location.href.search(/#[A-z0-9-_]*$/);
    for (let i=1; i < headers.length; i++){
        const headerId = headers[i].innerText.replace(/[ ]/g,'-').toLowerCase()
        headers[i].setAttribute('id', headerId);
        headers[i].addEventListener('click', () =>
            window.location.href = window.location.href.substring(0, scrollTargetIndex) + `#${headerId}`);
    }

    if (scrollTargetIndex > -1) {
        const scrollTarget = window.location.href.substring(scrollTargetIndex + 1);
        document.getElementById(scrollTarget).scrollIntoView({ behavior: "smooth" });
    }
});
