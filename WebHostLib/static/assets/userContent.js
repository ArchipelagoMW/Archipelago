window.addEventListener('load', () => {
  console.log("loaded");
  $("#rooms-table").DataTable({
        "paging": false,
        "ordering": true,
        "order": [[ 3, "desc" ]],
        "info": false,
        "dom": "t",
    });
  $("#seeds-table").DataTable({
        "paging": false,
        "ordering": true,
        "order": [[ 2, "desc" ]],
        "info": false,
        "dom": "t",
    });
});
