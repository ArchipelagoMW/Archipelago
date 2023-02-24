const adjustTableHeight = () => {
    const tablesContainer = document.getElementById('tables-container');
    const upperDistance = tablesContainer.getBoundingClientRect().top;

    const containerHeight = window.innerHeight - upperDistance;
    tablesContainer.style.maxHeight = `calc(${containerHeight}px - 1rem)`;

    const tableWrappers = document.getElementsByClassName('table-wrapper');
    for(let i=0; i < tableWrappers.length; i++){
        const maxHeight = (window.innerHeight - upperDistance) / 2;
        tableWrappers[i].style.maxHeight = `calc(${maxHeight}px - 1rem)`;
    }
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
        columnDefs: [
            {
                targets: 'hours',
                render: function (data, type, row) {
                    if (type === "sort" || type === 'type') {
                        if (data === "None")
                            return -1;

                        return parseInt(data);
                    }
                    if (data === "None")
                        return data;

                    let hours   = Math.floor(data / 3600);
                    let minutes = Math.floor((data - (hours * 3600)) / 60);

                    if (minutes < 10) {minutes = "0"+minutes;}
                    return hours+':'+minutes;
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
        target.load("/tracker/" + tracker, function (response, status) {
            if (status === "success") {
                target.find(".table").each(function (i, new_table) {
                    const new_trs = $(new_table).find("tbody>tr");
                    const old_table = tables.eq(i);
                    const topscroll = $(old_table.settings()[0].nScrollBody).scrollTop();
                    const leftscroll = $(old_table.settings()[0].nScrollBody).scrollLeft();
                    old_table.clear();
                    old_table.rows.add(new_trs).draw();
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

    $(".table-wrapper").scrollsync({
        y_sync: true,
        x_sync: true
    });

    adjustTableHeight();
});
