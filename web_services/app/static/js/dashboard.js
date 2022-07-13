$(document).ready(function() {
    var hash = localStorage.getItem("hash");
    if(hash == "get_advice"){
      $("#getAdvisorModal").modal({
          show: true,
          keyboard: false,
          backdrop: 'static'
      });
      $("#getAdvisorModal")
        .find('.close')
        .attr('onclick', 'show_confirmation_close_advice();')
        .removeAttr('data-dismiss');
    }
});

// Getting the News letter data
$("[name='event_anchor']").on('click', function(e){
    var type_of_event = $(this).attr('type-event');
    var event_id = $(this).attr('id');
    $.ajax({
        'method': 'POST',
        'url': '/news-letter',
        beforeSend: setHeader,
        'data':{
            'type_of_event' : type_of_event,
            'event_id': event_id
        },
        success: function(response){
            $('.newsletter-headline').html('');
            $('.newsletter-description').html('');
            response = response.event_data;
            var headline = response[0];
            if(headline){
                $("#newsLetterModalLabel").html('');
                $('.newsletter-headline')
                    .html(headline)
                    .removeClass('hide');
            }else{
                $("#newsLetterModalLabel").html('');
            }
            $('.newsletter-description').html(response[1]);
            show_bootstrap_modal('#newsLetter');
        },
        error: function(response){
            show_alert('error',
                "",
                '<p class="text-center">Unable to show the event</p>'
            );
        }
    });
});
