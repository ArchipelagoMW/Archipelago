window.addEventListener('load', () => {
  // Reload tracker
  const update = () => {
    // update items section
    const item_columns = document.getElementsByClassName('item-column');
    for (let i = 0; i < item_columns.length; i++) {
      $( item_columns[i].id ).load(' ' + item_columns[i].id);
    }

    // update locations section
    const location_columns = document.getElementsByClassName('location-column');
    for (let i = 0; i < location_columns.length; i++) {
      $( location_columns[i].id ).load(' ' + location_columns[i].id);
    }

    // update icons section
    const icon_columns = document.getElementsByClassName('icon-column');
    for (let i = 0; i < icon_columns.length; i++) {
      $( icon_columns[i].id ).load(' ' + icon_columns[i].id);
    }

    // update regions section
    const regions = document.getElementsByClassName('regions-column');
    for (let i = 0; i < regions.length; i++) {
      let region_name = regions[i].id;
      $( region_name ).load(' ' + region_name);
    }
  }

  setInterval(update, 15000);

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
