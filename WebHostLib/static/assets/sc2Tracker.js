let updateSection = (sectionName, fakeDOM) => {
    document.getElementById(sectionName).innerHTML = fakeDOM.getElementById(sectionName).innerHTML;
}

window.addEventListener('load', () => {
    // Reload tracker every 60 seconds (sync'd)
    const url = window.location;
    // Note: This synchronization code is adapted from code in trackerCommon.js
    const targetSecond = parseInt(document.getElementById('player-tracker').getAttribute('data-second')) + 3;
    console.log("Target second of refresh: " + targetSecond);

    let getSleepTimeSeconds = () => {
        // -40 % 60 is -40, which is absolutely wrong and should burn
        var sleepSeconds = (((targetSecond - new Date().getSeconds()) % 60) + 60) % 60;
        return sleepSeconds || 60;
    };

    let updateTracker = () => {
        const ajax = new XMLHttpRequest();
        ajax.onreadystatechange = () => {
            if (ajax.readyState !== 4) { return; }
    
            // Create a fake DOM using the returned HTML
            const domParser = new DOMParser();
            const fakeDOM = domParser.parseFromString(ajax.responseText, 'text/html');
    
            // Update dynamic sections
            updateSection('player-info', fakeDOM);
            updateSection('section-filler', fakeDOM);
            updateSection('section-terran', fakeDOM);
            updateSection('section-zerg', fakeDOM);
            updateSection('section-protoss', fakeDOM);
            updateSection('section-nova', fakeDOM);
            updateSection('section-kerrigan', fakeDOM);
            updateSection('section-keys', fakeDOM);
            updateSection('section-locations', fakeDOM);
        };
        ajax.open('GET', url);
        ajax.send();
        updater = setTimeout(updateTracker, getSleepTimeSeconds() * 1000);
    };
    window.updater = setTimeout(updateTracker, getSleepTimeSeconds() * 1000);
});
