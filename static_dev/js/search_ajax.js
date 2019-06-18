$('#search-form').submit(function (e) {
    $.post('/search/', $(this).serialize(), function (data) {
        $('.posts').html(data)
    });
    e.preventDefault();
});


