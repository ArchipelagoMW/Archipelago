window.addEventListener('load', () => {
    const tutorialWrapper = document.getElementById('tutorial-wrapper');
    new Promise((resolve, reject) => {
        const ajax = new XMLHttpRequest();
        ajax.onreadystatechange = () => {
            if (ajax.readyState !== 4) { return; }
            if (ajax.status === 404) {
                reject("Sorry, the tutorial is not available in that language yet.");
                return;
            }
            if (ajax.status !== 200) {
                reject("Something went wrong while loading the tutorial.");
                return;
            }
            resolve(ajax.responseText);
        };
        ajax.open('GET', `${window.location.origin}/static/assets/tutorial/tutorial_` +
            `${tutorialWrapper.getAttribute('data-language')}.md`, true);
        ajax.send();
    }).then((results) => {
        // Populate page with HTML generated from markdown
        tutorialWrapper.innerHTML = (new showdown.Converter()).makeHtml(results);

        // Reset the id of all header divs to something nicer
        const headers = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
        const scrollTargetIndex = window.location.href.search(/#[A-z0-9-_]*$/);
        for (let i=0; i < headers.length; i++){
            const headerId = headers[i].innerText.replace(/[ ]/g,'-').toLowerCase()
            headers[i].setAttribute('id', headerId);
            headers[i].addEventListener('click', () =>
                window.location.href = window.location.href.substring(0, scrollTargetIndex) + `#${headerId}`);
        }

        // Manually scroll the user to the appropriate header if anchor navigation is used
        if (scrollTargetIndex > -1) {
            try{
                const scrollTarget = window.location.href.substring(scrollTargetIndex + 1);
                document.getElementById(scrollTarget).scrollIntoView({ behavior: "smooth" });
            } catch(error) {
                console.error(error);
            }
        }
    }).catch((error) => {
        tutorialWrapper.innerHTML =
            `<h2>${error}</h2>
            <h3>Click <a href="${window.location.origin}/tutorial">here</a> to return to safety.</h3>`;
    });
});
