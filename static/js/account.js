function accept(id) {
    request = {"request_ID": id}
    $.get(request_accept_url, request, function(output) {
                location.reload();
            })
}
function decline(id) {
    request = {"request_ID": id}
    $.get(request_decline_url, request, function(output) {
                location.reload();
            })
}