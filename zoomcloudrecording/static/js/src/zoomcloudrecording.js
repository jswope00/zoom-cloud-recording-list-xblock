/* Javascript for ZoomCloudRecordingBlock. */
function ZoomCloudRecordingBlock(runtime, element) {
    try {
        $(element).find('#meeting_table').dataTable({
            "aoColumnDefs": [{ "bSortable": false, "aTargets": [ 0, 1, 2, 3 ] },
                             { "bSearchable": false, "aTargets": [ 0, 1, 2, 3 ] }],
            "bFilter": false,
            "bLengthChange": false,
            "sPaginationType": "full_numbers",
            "iDisplayLength": {page_size}
        });
    }
    catch(err) {}
}


