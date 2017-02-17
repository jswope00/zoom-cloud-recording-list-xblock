/* Javascript for ZoomCloudRecordingBlock. */
function ZoomCloudRecordingBlock(runtime, element) {
    try {
        var meeting_table = $(element).find('#meeting_table');
        // apply dataTable only if there are valid records
        if (meeting_table.find('tr').last().find('td')[0].innerHTML != "No Recordings") {
            meeting_table.dataTable({
                "aoColumnDefs": [{ "bSortable": false, "aTargets": [ 0, 1, 2, 3 ] },
                                 { "bSearchable": false, "aTargets": [ 0, 1, 2, 3 ] }],
                "bFilter": false,
                "bLengthChange": false,
                "sPaginationType": "full_numbers",
                "iDisplayLength": {page_size}
            });
	}
    }
    catch(err) {}
}


