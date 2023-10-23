window.addEventListener('load', () => {
  let tables = $(".autodatatable").DataTable({
        "paging": false,
        "ordering": true,
        "info": false,
        "dom": "t",
        "stateSave": true,
    });
  console.log(tables);
});
