window.addEventListener('load', () => {
  const url = window.location;
  setInterval(() => {
    const ajax = new XMLHttpRequest();
    ajax.onreadystatechange = () => {
      if (ajax.readyState !== 4) { return; }

      // Create a fake DOM using the returned HTML
      const domParser = new DOMParser();
      const fakeDOM = domParser.parseFromString(ajax.responseText, 'text/html');

      // Update item and location trackers
      document.getElementById('inventory-table').innerHTML = fakeDOM.getElementById('inventory-table').innerHTML;
      document.getElementById('location-table').innerHTML = fakeDOM.getElementById('location-table').innerHTML;

    };
    ajax.open('GET', url);
    ajax.send();
  }, 15000)
});
