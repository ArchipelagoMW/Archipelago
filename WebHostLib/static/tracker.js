window.addEventListener('load', () => {
    const tables = $(".table").DataTable({
        paging: false,
        info: false,
        scrollCollapse: true,

        // DO NOT use the scrollX or scrollY options. They cause DataTables to split the thead from
        // the tbody and render two separate tables.
    });

    const update = () => {
        const target = $("<div></div>");
        const tracker = document.getElementById('tracker-wrapper').getAttribute('data-tracker');
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
            } else {
                console.log("Failed to connect to Server, in order to update Table Data.");
                console.log(response);
            }
        })
    }

    setInterval(update, 30000);

    $(".dataTables_scrollBody").scrollsync({
        y_sync: true,
        x_sync: true
    });
});
