const domParser = new DOMParser();
const reloadTrackerDataInterval = 15000;
const loadTrackerData = async (url, dom) => {
  try {
    if (!dom) {
      const response = await fetch(url);
      const responseText = await response.text();
      dom = domParser.parseFromString(responseText, 'text/html');
    }

    const parsed = JSON.parse(dom.getElementById('script_data').text);
    document.getElementById('title').text = `${parsed.player_name}'s Tracker`;
    document.getElementById('day').textContent = parsed.day;
  } catch (error) {
    // log it, but don't let that stop the next interval
    console.error(error);
  }

  setTimeout(loadTrackerData, reloadTrackerDataInterval, url);
};

window.addEventListener('load', () => loadTrackerData(window.location, document));
