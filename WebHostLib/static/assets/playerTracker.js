window.addEventListener('load', () => {
  // Reload tracker
  const update = () => {
    const room = document.getElementById('tracker-wrapper').getAttribute('data-tracker');

    const request = new Request('/api/tracker/' + room);

    fetch(request)
    .then(response => response.json())
    .then(data => {
        // update locations blocks
        for (const location of data.checked_locations) {
            document.getElementById(location).classList.add('acquired');
        }
        // update totals checks done
        let total_checks_ele = document.getElementById('total-checks');
        const total_checks = document.getElementById('locations-container').children.length;
        let checks_done = data.checked_locations.length;
        total_checks_ele.innerText = 'Total Checks Done: ' + checks_done + '/' + total_checks;
        // update item and icons blocks
        for (const item in data.items_received) {
            if (document.getElementById(item)) {
                let current_item = document.getElementById(item);
                if (current_item.classList.contains('image-container')) {
                    current_item.children[0].classList.add('acquired');
                    current_item.children[1].innerText = item;
                } else {
                    current_item.innerText = item + data.items_received[item];
                }
            }
        }
    });
    }

    update()
    setInterval(update, 30000);


  // Collapsible regions section
  const regions = document.getElementsByClassName('regions-column');
  for (let i = 0; i < regions.length; i++) {
    let region_name = regions[i].id;
    if (region_name == 'Total') { continue; }

    const tab_header = document.getElementById(region_name+'-header');
    const locations = document.getElementById(region_name+'-locations');
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
