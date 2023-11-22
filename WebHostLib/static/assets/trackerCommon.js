const adjustTableHeight = () => {
    const tablesContainer = document.getElementById('tables-container');
    if (!tablesContainer)
        return;
    const upperDistance = tablesContainer.getBoundingClientRect().top;

    const tableWrappers = document.getElementsByClassName('table-wrapper');
    for (let i = 0; i < tableWrappers.length; i++) {
        // Ensure we are starting from maximum size prior to calculation.
        tableWrappers[i].style.height = null;
        tableWrappers[i].style.maxHeight = null;

        // Set as a reasonable height, but still allows the user to resize element if they desire.
        const currentHeight = tableWrappers[i].offsetHeight;
        const maxHeight = (window.innerHeight - upperDistance) / Math.min(tableWrappers.length, 4);
        if (currentHeight > maxHeight) {
            tableWrappers[i].style.height = `calc(${maxHeight}px - 1rem)`;
        }

        tableWrappers[i].style.maxHeight = `${currentHeight}px`;
    }
};

/**
 * Convert an integer number of seconds into a human readable HH:MM format
 * @param {Number} seconds
 * @returns {string}
 */
const secondsToHours = (seconds) => {
    let hours   = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds - (hours * 3600)) / 60).toString().padStart(2, '0');
    return `${hours}:${minutes}`;
};

window.addEventListener('load', () => {
    const tables = $(".table").DataTable({
        paging: false,
        info: false,
        dom: "t",
        stateSave: true,
        stateSaveCallback: function(settings, data) {
            delete data.search;
            localStorage.setItem(`DataTables_${settings.sInstance}_/tracker`, JSON.stringify(data));
        },
        stateLoadCallback: function(settings) {
            return JSON.parse(localStorage.getItem(`DataTables_${settings.sInstance}_/tracker`));
        },
        footerCallback: function(tfoot, data, start, end, display) {
            if (tfoot) {
                const activityData = this.api().column('lastActivity:name').data().toArray().filter(x => !isNaN(x));
                Array.from(tfoot?.children).find(td => td.classList.contains('last-activity')).innerText =
                  (activityData.length) ? secondsToHours(Math.min(...activityData)) : 'None';
            }
        },
        columnDefs: [
            {
                targets: 'last-activity',
                name: 'lastActivity'
            },
            {
                targets: 'hours',
                render: function (data, type, row) {
                    if (type === "sort" || type === 'type') {
                        if (data === "None")
                            return Number.MAX_VALUE;

                        return parseInt(data);
                    }
                    if (data === "None")
                        return data;

                    return secondsToHours(data);
                }
            },
            {
                targets: 'number',
                render: function (data, type, row) {
                    if (type === "sort" || type === 'type') {
                        return parseFloat(data);
                    }
                    return data;
                }
            },
            {
                targets: 'fraction',
                render: function (data, type, row) {
                    let splitted = data.split("/", 1);
                    let current = splitted[0]
                    if (type === "sort" || type === 'type') {
                        return parseInt(current);
                    }
                    return data;
                }
            },
        ],

        // DO NOT use the scrollX or scrollY options. They cause DataTables to split the thead from
        // the tbody and render two separate tables.
    });

    const searchBox = document.getElementById("search");
    searchBox.value = tables.search();
    searchBox.focus();
    searchBox.select();
    const doSearch = () => {
        tables.search(searchBox.value);
        tables.draw();
    };
    searchBox.addEventListener("keyup", doSearch);
    window.addEventListener("keydown", (event) => {
        if (!event.ctrlKey && !event.altKey && event.key.length === 1 && document.activeElement !== searchBox) {
            searchBox.focus();
            searchBox.select();
        }
        if (!event.ctrlKey && !event.altKey && !event.shiftKey && event.key === "Escape") {
            if (searchBox.value !== "") {
                searchBox.value = "";
                doSearch();
            }
            searchBox.blur();
            if (!document.getElementById("tables-container"))
                window.scroll(0, 0);
            event.preventDefault();
        }
    });
    const tracker = document.getElementById('tracker-wrapper').getAttribute('data-tracker');
    const target_second = document.getElementById('tracker-wrapper').getAttribute('data-second') + 3;

    function getSleepTimeSeconds(){
        // -40 % 60 is -40, which is absolutely wrong and should burn
        var sleepSeconds = (((target_second - new Date().getSeconds()) % 60) + 60) % 60;
        return sleepSeconds || 60;
    }

    const update = () => {
        const target = $("<div></div>");
        console.log("Updating Tracker...");
        target.load(location.href, function (response, status) {
            if (status === "success") {
                target.find(".table").each(function (i, new_table) {
                    const new_trs = $(new_table).find("tbody>tr");
                    const footer_tr = $(new_table).find("tfoot>tr");
                    const old_table = tables.eq(i);
                    const topscroll = $(old_table.settings()[0].nScrollBody).scrollTop();
                    const leftscroll = $(old_table.settings()[0].nScrollBody).scrollLeft();
                    old_table.clear();
                    if (footer_tr.length) {
                        $(old_table.table).find("tfoot").html(footer_tr);
                    }
                    old_table.rows.add(new_trs);
                    old_table.draw();
                    $(old_table.settings()[0].nScrollBody).scrollTop(topscroll);
                    $(old_table.settings()[0].nScrollBody).scrollLeft(leftscroll);
                });
                $("#multi-stream-link").replaceWith(target.find("#multi-stream-link"));
            } else {
                console.log("Failed to connect to Server, in order to update Table Data.");
                console.log(response);
            }
        })
        setTimeout(update, getSleepTimeSeconds()*1000);
    }
    setTimeout(update, getSleepTimeSeconds()*1000);

    window.addEventListener('resize', () => {
        adjustTableHeight();
        tables.draw();
    });

    adjustTableHeight();
});
