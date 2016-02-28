$("input[type='checkbox']").change(updateStatus);
$("h1").text('Fuck you');
function updateStatus(){
    $("h1").text('Fuck you');
    // var params = {}
    // params[$(this).prop('name')] = $(this).prop('checked');
    // params['movie_id'] = $(this).data('id');
    params = {}
    $.post('/set_status',
    {
        params
    });
}
