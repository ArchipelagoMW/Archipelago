window.addEventListener('load', () => {
    const gameSettings = document.getElementById('game-settings');
    new Promise((resolve, reject) => {
        const ajax = new XMLHttpRequest();
        ajax.onreadystatechange = () => {
            if (ajax.readyState !== 4) { return; }
            if (ajax.status !== 200) {
                reject("Unable to fetch source yaml file.");
                return;
            }
            resolve(ajax.responseText);
        };
        ajax.open('GET', `${window.location.origin}/static/static/easy.yaml` ,true);
        ajax.send();
    }).then((results) => {
        // Load YAML into object
        const sourceData = jsyaml.load(results);

        // Update localStorage with three settings objects. Preserve original objects if present.
        for (let i=1; i<=3; i++) {
            const localSettings = localStorage.getItem(`gameSettings${i}`);
            const updatedObj = localSettings ? Object.assign(sourceData, JSON.parse(localSettings)) : sourceData;
            localStorage.setItem(`gameSettings${i}`, JSON.stringify(updatedObj));
        }

        console.info(sourceData);
    }).catch((error) => {
        gameSettings.innerHTML = `
        <h2>Something went wrong while loading your game settings page.</h2>
        <h2>${error}</h2>
        <h2><a href="${window.location.origin}">Click here to return to safety!</a></h2>
        `
    });
});
