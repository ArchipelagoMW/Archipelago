"use strict";
class Payload {
    get rat_count() {
        return this.inventory['Normal Rat'] + (this.inventory['Entire Rat Pack'] * 5);
    }

    markFoundIf(prop, classNameSuffix) {
        if (prop(this) > 0) {
            for (const container of document.getElementsByClassName(`received-${classNameSuffix}`)) {
                container.classList.remove('not-found');
            }
        }
    }
}

const domParser = new DOMParser();
const reloadTrackerDataInterval = 15000;
const loadTrackerData = async (url, dom) => {
    try {
        if (!dom) {
            const response = await fetch(`${url}`);
            const responseText = await response.text();
            dom = domParser.parseFromString(responseText, 'text/html');
        }

        const parsedRaw = JSON.parse(dom.getElementById('script-data').text);
        const parsed = Object.assign(new Payload(), parsedRaw);
        document.getElementById('title').text = `${parsed.player_name}'s Tracker`;
        document.getElementById('rat-count').textContent = `${parsed.rat_count}`;
        parsed.markFoundIf(x => x.rat_count, 'normal-rat');
        parsed.markFoundIf(x => x.inventory['Pack Rat'], 'pack-rat');
        parsed.markFoundIf(x => x.inventory['Pizza Rat'], 'pizza-rat');
        parsed.markFoundIf(x => x.inventory['Chef Rat'], 'chef-rat');
        parsed.markFoundIf(x => x.inventory['Ninja Rat'], 'ninja-rat');
        parsed.markFoundIf(x => x.inventory['Gym Rat'], 'gym-rat');
        parsed.markFoundIf(x => x.inventory['Computer Rat'], 'computer-rat');
        parsed.markFoundIf(x => x.inventory['Pie Rat'], 'pie-rat');
        parsed.markFoundIf(x => x.inventory['Ziggu Rat'], 'ziggu-rat');
        parsed.markFoundIf(x => x.inventory['Acro Rat'], 'acro-rat');
        parsed.markFoundIf(x => x.inventory['Lab Rat'], 'lab-rat');
        parsed.markFoundIf(x => x.inventory['Soc-Rat-es'], 'soc-rat-es');
        parsed.markFoundIf(x => x.inventory['A Cookie'], 'a-cookie');
        parsed.markFoundIf(x => x.inventory['Fresh Banana Peel'], 'fresh-banana-peel');
        parsed.markFoundIf(x => x.inventory['MacGuffin'], 'macguffin');
        parsed.markFoundIf(x => x.inventory['Blue Turtle Shell'], 'blue-turtle-shell');
        parsed.markFoundIf(x => x.inventory['Red Matador\'s Cape'], 'red-matador-cape');
        parsed.markFoundIf(x => x.inventory['Pair of Fake Mouse Ears'], 'pair-of-fake-mouse-ears');
        parsed.markFoundIf(x => x.inventory['Bribe'], 'bribe');
        parsed.markFoundIf(x => x.inventory['Masterful Longsword'], 'masterful-longsword');
        parsed.markFoundIf(x => x.inventory['Legally Binding Contract'], 'legally-binding-contract');
        parsed.markFoundIf(x => x.inventory['Priceless Antique'], 'priceless-antique');
        parsed.markFoundIf(x => x.inventory['Premium Can of Prawn Food'], 'premium-can-of-prawn-food');
    }
    catch (error) {
        // log it, but don't let that stop the next interval
        console.error(error);
    }
    setTimeout(loadTrackerData, reloadTrackerDataInterval, url);
};

window.addEventListener('load', () => loadTrackerData(window.location, document));
