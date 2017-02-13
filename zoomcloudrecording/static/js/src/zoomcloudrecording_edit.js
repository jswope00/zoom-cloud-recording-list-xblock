/* Javascript for ZoomCloudRecordingEditBlock. */
function ZoomCloudRecordingEditBlock(runtime, element) {

    $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    var host_id = $(element).find('input[name=host_id]').val();
    if (host_id != '') {
        var data = {
          host_id: host_id,
          meeting_number: $(element).find('input[name=meeting_number]').val(),
          from_date: $(element).find('input[name=from_date]').val(),
          to_date: $(element).find('input[name=to_date]').val(),
          page_size: $(element).find('input[name=page_size]').val(),
          page_number: $(element).find('input[name=page_number]').val()
        };
        runtime.notify('save', {state: 'start'});
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
          runtime.notify('save', {state: 'end'});
        });
    }
    else {
        alert('Host ID is empty');
    }
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });

}
