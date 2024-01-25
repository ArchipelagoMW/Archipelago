"use strict";
class Payload {
    get current_region_classes() {
        let currentRegion = this.game_state.current_region;
        if (currentRegion == 'Traveling') {
            currentRegion = this.game_state.destination_region;
        }

        switch (currentRegion) {
            case 'Before8Rats':
                return ['before-basketball'];

            case 'Gate8Rats':
                return ['checked-basketball'];

            case 'After8RatsBeforeA':
                return ['before-minotaur-maze'];

            case 'After8RatsBeforeB':
                return ['before-restaurant'];

            case 'A':
                return ['checked-minotaur-maze'];

            case 'B':
                return ['checked-restaurant'];

            case 'AfterABeforeC':
                return ['before-prawn-stars'];

            case 'AfterBBeforeD':
                return ['before-heavy-boulder'];

            case 'C':
                return ['checked-prawn-stars'];

            case 'D':
                return ['checked-heavy-boulder'];

            case 'AfterCBefore20Rats':
                return ['before-bowling-ball-door', 'after-prawn-stars'];

            case 'AfterDBefore20Rats':
                return ['before-bowling-ball-door', 'after-heavy-boulder'];

            case 'Gate20Rats':
                return ['checked-bowling-ball-door'];

            case 'After20RatsBeforeE':
                return ['before-captured-goldfish'];

            case 'After20RatsBeforeF':
                return ['before-computer-pad'];

            case 'E':
                return ['checked-captured-goldfish'];

            case 'F':
                return ['checked-computer-pad'];

            case 'TryingForGoal':
                return ['checked-goal'];

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
        parsed.markCheckedIf(() => checked_locations.has('g8r'), 'basketball');
        parsed.markCheckedIf(() => checked_locations.has('a'), 'minotaur-maze');
        parsed.markCheckedIf(() => checked_locations.has('b'), 'restaurant');
        parsed.markCheckedIf(() => checked_locations.has('c'), 'prawn-stars');
        parsed.markCheckedIf(() => checked_locations.has('d'), 'heavy-boulder');
        parsed.markCheckedIf(() => checked_locations.has('g20r'), 'bowling-ball-door');
        parsed.markCheckedIf(() => checked_locations.has('e'), 'captured-goldfish');
        parsed.markCheckedIf(() => checked_locations.has('f'), 'computer-pad');
        parsed.markCheckedIf(() => checked_locations.has('goal'), 'goal');

        parsed.markLocationOpenIf(x => x.rat_count >= 8, 'basketball');
        parsed.markLocationOpenIf(x => checked_locations.has('g8r') && x.inventory['A Cookie'] > 0, 'minotaur-maze');
        parsed.markLocationOpenIf(x => checked_locations.has('g8r') && x.inventory['Fresh Banana Peel'] > 0, 'restaurant');
        parsed.markLocationOpenIf(x => checked_locations.has('a') && x.inventory['MacGuffin'] > 0, 'prawn-stars');
        parsed.markLocationOpenIf(x => checked_locations.has('b') && x.inventory['Blue Turtle Shell'] > 0, 'heavy-boulder');
        parsed.markLocationOpenIf(x => x.rat_count >= 20 && (checked_locations.has('c') || checked_locations.has('d')), 'bowling-ball-door');
        parsed.markLocationOpenIf(x => checked_locations.has('g20r') && x.inventory['Red Matador\'s Cape'] > 0, 'captured-goldfish');
        parsed.markLocationOpenIf(x => checked_locations.has('g20r') && x.inventory['Pair of Fake Mouse Ears'] > 0, 'computer-pad');
        parsed.markLocationOpenIf(() => checked_locations.has('e') || checked_locations.has('f'), 'goal');

        parsed.markPathOpenIf(x => checked_locations.has('g8r'), 'minotaur-maze');
        parsed.markPathOpenIf(x => checked_locations.has('g8r'), 'restaurant');
        parsed.markPathOpenIf(x => checked_locations.has('a'), 'prawn-stars');
        parsed.markPathOpenIf(x => checked_locations.has('b'), 'heavy-boulder');
        parsed.markPathOpenIf(x => checked_locations.has('c'), 'bowling-ball-door after-prawn-stars');
        parsed.markPathOpenIf(x => checked_locations.has('d'), 'bowling-ball-door after-heavy-boulder');
        parsed.markPathOpenIf(x => checked_locations.has('g20r'), 'captured-goldfish');
        parsed.markPathOpenIf(x => checked_locations.has('g20r'), 'computer-pad');
        parsed.markPathOpenIf(x => checked_locations.has('e'), 'goal after-captured-goldfish');
        parsed.markPathOpenIf(x => checked_locations.has('f'), 'goal after-computer-pad');

        const { stepInterval } = parsed.aura_modifiers;
        for (const container of document.getElementsByClassName('movement-speed-text')) {
            container.textContent = `${1 / stepInterval}x`;
        }

        if (!(completedGoal = parsed.completed_goal)) {
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
