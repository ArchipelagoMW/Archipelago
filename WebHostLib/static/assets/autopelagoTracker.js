"use strict";
class Payload {
    get current_region_classes() {
        let currentRegion = this.game_state.current_region;
        if (currentRegion == 'Traveling') {
            currentRegion = this.game_state.destination_region;
        }

        switch (currentRegion) {
            case 'BeforeBasketball':
                return ['before-basketball'];

            case 'Basketball':
                return ['checked-basketball'];

            case 'BeforeMinotaur':
                return ['before-minotaur'];

            case 'BeforePrawnStars':
                return ['before-prawn-stars'];

            case 'Minotaur':
                return ['checked-minotaur'];

            case 'PrawnStars':
                return ['checked-prawn-stars'];

            case 'BeforeRestaurant':
                return ['before-restaurant'];

            case 'BeforePirateBakeSale':
                return ['before-pirate-bake-sale'];

            case 'Restaurant':
                return ['checked-restaurant'];

            case 'PirateBakeSale':
                return ['checked-pirate-bake-sale'];

            case 'AfterRestaurant':
                return ['after-restaurant'];

            case 'AfterPirateBakeSale':
                return ['after-pirate-bake-sale'];

            case 'BowlingBallDoor':
                return ['checked-bowling-ball-door'];

            case 'BeforeGoldfish':
                return ['before-captured-goldfish'];

            case 'Goldfish':
                return ['checked-captured-goldfish'];

            default:
                return [];
        }
    }

    get aura_modifiers() {
        let stepInterval = 1;
        for (const aura of this.game_state.auras ?? []) {
            if (aura["$type"] == "stepInterval") {
                stepInterval *= aura.modifier;
            }
        }

        return {
            stepInterval: stepInterval,
        };
    }

    get completed_goal() {
        return this.game_state.current_region == 'CompletedGoal';
    }

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

    markPathOpenIf(prop, classNameSuffix) {
        if (prop(this)) {
            for (const container of document.getElementsByClassName(`before-${classNameSuffix}`)) {
                container.classList.remove('not-open');
            }
        }
    }

    markLocationOpenIf(prop, classNameSuffix) {
        if (prop(this)) {
            for (const container of document.getElementsByClassName(`checked-${classNameSuffix}`)) {
                container.classList.remove('not-open');
            }
        }
    }

    markCheckedIf(prop, classNameSuffix) {
        if (prop(this)) {
            for (const container of document.getElementsByClassName(`checked-${classNameSuffix}`)) {
                container.classList.remove('not-checked');
            }
        }
    }
}

const domParser = new DOMParser();
const reloadTrackerDataInterval = 1000; // FOR NOW
const loadTrackerData = async (url, dom) => {
    let completedGoal = false;
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

        const checked_locations = new Set(parsed.checked_locations);
        parsed.markCheckedIf(() => checked_locations.has('basketball'), 'basketball');
        parsed.markCheckedIf(() => checked_locations.has('minotaur'), 'minotaur');
        parsed.markCheckedIf(() => checked_locations.has('prawn stars'), 'prawn-stars');
        parsed.markCheckedIf(() => checked_locations.has('restaurant'), 'restaurant');
        parsed.markCheckedIf(() => checked_locations.has('pirate bake sale'), 'pirate-bake-sale');
        parsed.markCheckedIf(() => checked_locations.has('bowling ball door'), 'bowling-ball-door');
        parsed.markCheckedIf(() => checked_locations.has('goldfish'), 'captured-goldfish');

        parsed.markLocationOpenIf(x => x.rat_count >= 5, 'basketball');
        parsed.markLocationOpenIf(x => checked_locations.has('basketball') && x.inventory['Red Matador\'s Cape'] > 0, 'minotaur');
        parsed.markLocationOpenIf(x => checked_locations.has('basketball') && x.inventory['Premium Can of Prawn Food'] > 0, 'prawn-stars');
        parsed.markLocationOpenIf(x => checked_locations.has('minotaur') && x.inventory['A Cookie'] > 0, 'restaurant');
        parsed.markLocationOpenIf(x => checked_locations.has('prawn-stars') && x.inventory['Bribe'] > 0, 'pirate-bake-sale');
        parsed.markLocationOpenIf(x => x.rat_count >= 20 && (checked_locations.has('restaurant') || checked_locations.has('pirate-bake-sale')), 'bowling-ball-door');
        parsed.markLocationOpenIf(x => checked_locations.has('bowling-ball-door') && x.inventory['Masterful Longsword'] > 0, 'captured-goldfish');

        parsed.markPathOpenIf(x => checked_locations.has('basketball'), 'minotaur');
        parsed.markPathOpenIf(x => checked_locations.has('basketball'), 'prawn-stars');
        parsed.markPathOpenIf(x => checked_locations.has('minotaur'), 'restaurant');
        parsed.markPathOpenIf(x => checked_locations.has('prawn-stars'), 'pirate-bake-sale');
        parsed.markPathOpenIf(x => checked_locations.has('restaurant'), 'bowling-ball-door after-restaurant');
        parsed.markPathOpenIf(x => checked_locations.has('pirate-bake-sale'), 'bowling-ball-door after-pirate-bake-sale');
        parsed.markPathOpenIf(x => checked_locations.has('bowling-ball-door'), 'captured-goldfish');

        const { stepInterval } = parsed.aura_modifiers;
        for (const container of document.getElementsByClassName('movement-speed-text')) {
            container.textContent = `${1 / stepInterval}x`;
        }

        if (completedGoal = parsed.completed_goal) {
            for (const container of document.getElementsByClassName('current-region')) {
                container.classList.remove('current-region');
            }

            for (const container of document.getElementsByClassName('checked-captured-goldfish')) {
                container.classList.add('current-region');
            }
        } else {
            const currentRegionClasses = parsed.current_region_classes;
            let needsChange = false;
            for (const container of document.getElementsByClassName('current-region')) {
                for (const currentRegionClass of currentRegionClasses) {
                    if (!container.classList.contains(currentRegionClass)) {
                        container.classList.remove('current-region');
                        needsChange = true;
                    }
                }
            }

            if (needsChange) {
                for (const container of document.getElementsByClassName(currentRegionClasses.join(' '))) {
                    container.classList.add('current-region');
                }
            }
        }
    }
    catch (error) {
        // log it, but don't let that stop the next interval
        console.error(error);
    }

    if (!completedGoal) {
        setTimeout(loadTrackerData, reloadTrackerDataInterval, url);
    }
};

window.addEventListener('load', () => loadTrackerData(window.location, document));
