let updateSection = (sectionName, fakeDOM) => {
    document.getElementById(sectionName).innerHTML = fakeDOM.getElementById(sectionName).innerHTML;
}

window.addEventListener('load', () => {
    // Reload tracker every 15 seconds
    const url = window.location;
    window.refreshInterval = setInterval(() => {
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
    }, 15000)
});
