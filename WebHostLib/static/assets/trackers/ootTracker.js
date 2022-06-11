window.addEventListener('load', () => {
  // Reload tracker every 15 seconds
  const url = window.location;
  setInterval(() => {
    const ajax = new XMLHttpRequest();
    ajax.onreadystatechange = () => {
      if (ajax.readyState !== 4) { return; }

      // Create a fake DOM using the returned HTML
      const domParser = new DOMParser();
      const fakeDOM = domParser.parseFromString(ajax.responseText, 'text/html');

      // Update item tracker
      document.getElementById('inventory-table').innerHTML = fakeDOM.getElementById('inventory-table').innerHTML;
      // Update only counters, small keys, and boss keys in the location-table
      const types = ['counter', 'smallkeys', 'bosskeys'];
      for (let j = 0; j < types.length; j++) {
        let counters = document.getElementsByClassName(types[j]);
        const fakeCounters = fakeDOM.getElementsByClassName(types[j]);
        for (let i = 0; i < counters.length; i++) {
          counters[i].innerHTML = fakeCounters[i].innerHTML;
        }
      }
    };
    ajax.open('GET', url);
    ajax.send();
  }, 15000)

  // Collapsible advancement sections
  const categories = document.getElementsByClassName("location-category");
  for (let i = 0; i < categories.length; i++) {
    let hide_id = categories[i].id.split('-')[0];
    if (hide_id == 'Total') {
      continue;
    }
    categories[i].addEventListener('click', function() {
      // Toggle the advancement list
      document.getElementById(hide_id).classList.toggle("hide");
      // Change text of the header
      const tab_header = document.getElementById(hide_id+'-header').children[0];
      const orig_text = tab_header.innerHTML;
      let new_text;
      if (orig_text.includes("▼")) {
        new_text = orig_text.replace("▼", "▲");
      }
      else {
        new_text = orig_text.replace("▲", "▼");
      }
      tab_header.innerHTML = new_text;
    });
  }
});
