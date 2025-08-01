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
        ajax.open('GET', `${window.location.origin}/static/generated/docs/` +
            `${tutorialWrapper.getAttribute('data-game')}/${tutorialWrapper.getAttribute('data-file')}_` +
            `${tutorialWrapper.getAttribute('data-lang')}.md`, true);
        ajax.send();
    }).then((results) => {
        // Populate page with HTML generated from markdown
        showdown.setOption('tables', true);
        showdown.setOption('strikethrough', true);
        showdown.setOption('literalMidWordUnderscores', true);
        showdown.setOption('disableForced4SpacesIndentedSublists', true);
        tutorialWrapper.innerHTML += (new showdown.Converter()).makeHtml(results);

        const title = document.querySelector('h1')
        if (title) {
            document.title = title.textContent;
        }

        // Reset the id of all header divs to something nicer
        for (const header of document.querySelectorAll('h1, h2, h3, h4, h5, h6')) {
            const headerId = header.innerText.replace(/\s+/g, '-').toLowerCase();
            header.setAttribute('id', headerId);
            header.addEventListener('click', () => {
                window.location.hash = `#${headerId}`;
                header.scrollIntoView();
            });
        }

        // Manually scroll the user to the appropriate header if anchor navigation is used
        document.fonts.ready.finally(() => {
            if (window.location.hash) {
                const scrollTarget = document.getElementById(window.location.hash.substring(1));
                scrollTarget?.scrollIntoView();
            }
        });
    });
});
