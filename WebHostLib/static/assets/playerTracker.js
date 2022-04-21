window.addEventListener('load', () => {
  // Reload tracker
  const update = () => {
    const url = document.getElementById('tracker-wrapper').getAttribute('data-tracker');

    fetch('/tracker/' + url, {
        method: "GET"
    }).then(function (response) {
        return response.text()
    }).then(function (html) {
        document.body.innerHTML = html;
    //    var parser = new DOMParser();
    //    var doc = parser.parseFromString(html, "text/html");
//
    //const items = document.getElementsByClassName('item-column');
    //for (let i = 0; items.length; i++){
    //    items[i] = doc.querySelector('#' + items[i].id);
    //}
//
    //const locations = document.getElementsByClassName('location-column');
    //for (let i = 0; locations.length; i++){
    //    locations[i] = doc.querySelector('#' + locations[i].id);
    //}
//
    //const regions = document.getElementsByClassName('regions-column');
    //for (let i = 0; regions.length; i++){
    //    regions[i] = doc.querySelector('#' + regions[i].id);
    //}
    //});
  }

  setInterval(update, 30000);

  // Collapsible regions section
  const regions = document.getElementsByClassName('regions-column');
  for (let i = 0; i < regions.length; i++) {
    let region_name = regions[i].id;
    if (region_name == 'Total') { continue; }

    const tab_header = document.getElementById(region_name+'-header');
    const locations = document.getElementById(region_name+'-locations')
    // toggle locations display
    regions[i].addEventListener('click', function(event) {
      if (tab_header.innerHTML.includes("▼")) {
          locations.classList.remove('hidden');
          // change header text
          tab_header.innerHTML = tab_header.innerHTML.replace('▼', '▲');
      } else {
          locations.classList.add('hidden');
          // change header text
          tab_header.innerHTML = tab_header.innerHTML.replace('▲', '▼');
      }
    });
  }
  });
