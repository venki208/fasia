var add_event_btn = $('button[name="add_event"]');
var submit_event_btn = $('button[name="submit_event"]');
var update_event_btn = $('button[name="update_event_btn"]');
var delete_event_btn = $("button[name='delete_event_btn']");
var end_date_clr_btn = $(".remove-end-date");
var viewed_title, viewed_description, viewed_start_date, viewed_end_date;

// Intializing the calender
$('#calendar').fullCalendar({
    displayEventTime: false,
    eventLimit: true,
    // themeSystem: 'bootstrap3',
    header: {
        left: '',
        center: 'title',
        right: 'today,month,listWeek,prev,next'
    },
    events: function(start, end, timezone, callback) {
        $.ajax({
            method: 'GET',
            url: '/calendar-events',
            beforeSend: setHeader,
            data: {},
            success: function(response) {
                var color_code = 'default';
                var events = [];
                var data = response.data.advisor_events;
                for(i=0; i<data.length; i++){
                    var end_date;
                    try{
                        end_date = data[i].end_date.$date;
                    }catch(e){
                        end_date = data[i].start_date.$date;
                    }
                    if(data[i].user_type == 'fasia_admin'){
                        color_code = '#f4941e';
                    }else{
                        color_code = 'default';
                    }
                    events.push({
                        id: data[i]._id.$oid,
                        title: data[i].event_name,
                        start: data[i].start_date.$date,
                        description: data[i].description,
                        end: end_date,
                        user_type: data[i].user_type,
                        color: color_code
                    });
                }
                callback(events);
            }
        });
    }
});

// Getting clicked date information
var calendar = $('#calendar').fullCalendar('getCalendar');
calendar.on('dayClick', function(date, jsEvent, view) {
    console.log('clicked on ' + date.format());
});

// showing extra information about the event
calendar.on('eventClick', function(cal_event, jsEvent, view){
    viewed_title = cal_event.title;
    viewed_start_date = String(cal_event.start._d.getDate())+'-'+String(cal_event.start._d.getMonth()+1)+'-'+String(cal_event.start._d.getFullYear());
    if(cal_event.end){
        viewed_end_date = String(cal_event.end._d.getDate())+'-'+String(cal_event.end._d.getMonth()+1)+'-'+String(cal_event.end._d.getFullYear());
    }else{
        viewed_end_date = '';
    }
    viewed_description = cal_event.description;
    if (!viewed_description){
        viewed_description = 'No event description';
    }
    $("#eventInformationModalLabel").html(cal_event.title);
    $("#event_description_div").html(
        "<p>"+viewed_description+"</p>"
    );
    // advisor can able edit only his events
    if(cal_event.user_type != 'advisor'){
        update_event_btn.hide();
        delete_event_btn.hide();
    }else{
        update_event_btn
            .attr('id', cal_event.id)
            .show();
        delete_event_btn
            .attr('event_id', cal_event.id)
            .show();
    }
    show_bootstrap_modal('#event_information');
});

// Showing modal for adding new event
add_event_btn.on('click', function(e){
    $("[name='event_form']")[0].reset();
    submit_event_btn.html('Add');
    $("#start_date")
        .datepicker("option", "minDate", new Date())
        .datepicker("option", "maxDate", null);
    $("#end_date")
        .datepicker("option", "minDate", new Date())
        .datepicker("option", "maxDate", null);
    show_bootstrap_modal('#add_event_modal');
});

// attaching datepicker to date of birth
var altFormat = $("#start_date").datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: "dd-mm-yy",
    minDate: "Date()",
    onSelect: function (selected) {
        var end_date = $('#start_date').datepicker('getDate');
        end_date.setDate(end_date.getDate() + 1);
        $("#end_date").datepicker("option", "minDate", end_date);
    }
});

// attaching datepicker to date of birth
var altFormat = $("#end_date").datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: "dd-mm-yy",
    minDate: "Date()",
    onSelect: function (selected) {
        $(".remove-end-date").removeClass('hide');
        var end_date = $('#end_date').datepicker('getDate');
        end_date.setDate(end_date.getDate() - 1);
        $("#start_date").datepicker("option", "maxDate", end_date);
    }
});

// Blocking user to edit through keyboard
$('#start_date, #end_date').on('keypress focus', function(e) {
    $(this).attr('readonly', true);
    e.preventDefault(); // Don't allow direct editing
});
$('#start_date, #end_date').on('focusout', function(e) {
    $(this).removeAttr('readonly');
});

// Adding and updating the calender
submit_event_btn.on('click', function(e){
    var final_end_date;
    var event_id = $("[name='event_id']").val();
    var event_name = $('[name="event_name"]').val();
    var start_date = $('[name="start_date"]').val();
    var end_date = $('[name="end_date"]').val();
    if (end_date){
        final_end_date = end_date+' 23:59';
    }else{
        final_end_date = end_date;
    }
    var event_description = $('[name="event_description"]').val();
    $.ajax({
        method: 'POST',
        url: '/calendar-events',
        beforeSend: setHeader,
        data: {
            event_id: event_id,
            event_name : event_name,
            start_date : start_date,
            end_date : final_end_date,
            description: event_description,
            user_type : 'advisor'
        },
        success: function(e){
            if(e.status == 'success'){
                start_date = $('#start_date').datepicker('getDate');
                if (end_date == ''){
                    end_date = start_date;
                }else{
                    end_date = end_date.split('-');
                    end_date = new Date(end_date[2], parseInt(end_date[1])-1, end_date[0], 23, 59);
                }
                var newEvent = {
                    title: event_name,
                    start: start_date,
                    end: end_date,
                    description: event_description,
                    id: e.ev_id,
                    user_type: e.user_type
                };
                if (event_id == ''){
                    $('#calendar').fullCalendar( 'renderEvent', newEvent);
                }else{
                    var update_event = $("#calendar").fullCalendar('clientEvents', e.ev_id);
                    update_event[0].title = event_name;
                    update_event[0].start = start_date;
                    update_event[0].end = end_date;
                    update_event[0].description = event_description;
                    $('#calendar').fullCalendar('updateEvent', update_event[0]);
                }
                $('#add_event_modal').modal('hide');
                event_id = '';
                $("[name='event_id']").val('');
            }
        },
        error: function(e){
            alert('Unable to add Event \n Please try again after sometime');
        }
    });
});

// showing edit modal for update the event
update_event_btn.on('click', function(){
    $("#event_information").modal('hide');
    $("input[name='event_id']").val(update_event_btn.attr('id'));
    $("input[name='event_name']").val(viewed_title);
    $("[name='event_description']").val(viewed_description);
    $("input[name='start_date']").val(viewed_start_date);
    $("input[name='end_date']").val(viewed_end_date);
    submit_event_btn.html('Update');
    show_bootstrap_modal('#add_event_modal');
});

// deleting the event from calender
delete_event_btn.on('click', function(e){
    var del_event_id = $(this).attr('event_id');
    $('#calendar').fullCalendar('removeEvents', [del_event_id]);
    $.ajax({
        method: 'DELETE',
        url: '/calendar-events',
        beforeSend: setHeader,
        data:{
            event_id : del_event_id
        },
        success:function(response){
            if (response == 'success'){
                $("#event_information").modal('hide');
            }else{
                alert('Unable to delete the event \n Please try again after some time');
            }
        },
        error: function(e){
            alert('Unable to delete the event \n Please try again after some time');
        }
    });
});

// Setting datepicker events to default after closing the modal
$("#add_event_modal").on('hidden.bs.modal', function (e) {
    $("#start_date").datepicker('option', 'minDate', 0);
    $("#end_date").datepicker('option', 'minDate', 0);
});

// clear the expire date field
end_date_clr_btn.on('click', function(e){
    $("#end_date").val('');
    $(this).addClass('hide');
});