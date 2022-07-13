// var add_event_btn = $('button[name="add_event"]');
var submit_event_btn = $('button[name="create_event"]');
var list_events_link = $("#list_events_link");
var update_event_btn = $('button[name="update_event_btn"]');
var delete_event_btn = $("button[name='delete_event_btn']");
var viewed_title, viewed_description, viewed_start_date, viewed_end_date;
var event_id_td, event_name_td, event_description_td, start_date_td, end_date_td;

$('#calendar').fullCalendar({
    displayEventTime: false,
    eventLimit: true,
    header:{
        left: 'today prev,next',
        center: 'title',
        right: 'month,listWeek'
    },
    // themeSystem : 'bootstrap3',
    events: function(start, end, timezone, callback) {
        $.ajax({
            method: 'GET',
            url: '/auth/admin-dashboard/calendar_event',
            data: {},
            success: function(response) {
                var events = [];
                var data = response.data.advisor_events;
                for(i=0; i<data.length; i++){
                    var end_date;
                    try{
                        end_date = data[i].end_date.$date;
                    }catch(e){
                        end_date = data[i].start_date.$date;
                    }
                    events.push({
                        id: data[i]._id.$oid,
                        title: data[i].event_name,
                        start: data[i].start_date.$date,
                        description: data[i].description,
                        end: end_date
                    });
                }
                callback(events);
            }
        });
    }
});


var calendar = $('#calendar').fullCalendar('getCalendar');
calendar.on('dayClick', function(date, jsEvent, view) {
    console.log('clicked on ' + date.format());
});

// Loading the modal for adding the event
function event_modal() {
    $("input[name='event_id']").val(this.id);
    submit_event_btn.html('CREATE');
    show_bootstrap_modal('#admin_event_modal');
}

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
        var end_date = $('#end_date').datepicker('getDate');
        end_date.setDate(end_date.getDate() - 1);
        $("#start_date").datepicker("option", "maxDate", end_date);
    }
});

$('#start_date, #end_date').on('keypress focus', function(e) {
    $(this).attr('readonly', true);
    e.preventDefault(); // Don't allow direct editing
});

$('#start_date, #end_date').on('focusout', function(e) {
    $(this).removeAttr('readonly');
});

function validate_event_form() {
    var event_description = validate_field_onkeypress('event_description', 'help_event_description', 'Event Description');
    var end_date = validate_field_onkeypress('end_date', 'help_end_date', 'End Date');
    var start_date = validate_field_onkeypress('start_date', 'help_start_date', 'Start Date');
    var event_name = validate_field_onkeypress('event_name', 'help_event_name', 'Event Name');
    if(event_name !=0 || start_date != 0 || end_date != 0 || event_description != 0){
        return false;
    }else{
        return true;
    }
}


// Validating the create or update event form and submitting the result
submit_event_btn.on("click", function(e) {
    var final_end_date;
    var event_id = $("[name='event_id']").val();
    var event_name = $('[name="event_name"]').val();
    var start_date = $('[name="start_date"]').val();
    var end_date = $('[name="end_date"]').val();
    if(end_date){
        final_end_date = end_date+' 23:59'; 
    }else{
        final_end_date = end_date;
    }
    var event_description = $('[name="event_description"]').val();
    if(validate_event_form()){
        $.ajax({
            type : 'POST',
            url : '/auth/admin-dashboard/calendar_event',
            data :{
                'event_id'   : event_id,
                'event_name' : event_name,
                'start_date' : start_date,
                'end_date'   : final_end_date,
                'description' : event_description,
            },
            success: function(response) {
                if (response.status == 'success') {
                    start_date = $('#start_date').datepicker('getDate');
                    if (end_date == '') {
                        end_date = start_date;
                    } else {
                        end_date = end_date.split('-');
                        end_date = new Date(end_date[2], parseInt(end_date[1]) - 1, end_date[0], 23, 59);
                    }
                    var newEvent = {
                        title: event_name,
                        start: start_date,
                        end: end_date,
                        description: event_description,
                        id: response.ev_id,
                    };
                    // if event id is empty means creating new event else request is updating the event
                    if (event_id == '') {
                        // attaching event to calender
                        $('#calendar').fullCalendar('renderEvent', newEvent);
                        // attching event to list table
                        $(".list_calender_table").find('tbody').append(
                            '<tr>'+
                                '<td>'+
                                    event_name+
                                '</td>'+
                                '<td>'+
                                    event_description+
                                '</td>'+
                                '<td>'+
                                    $('[name="start_date"]').val()+
                                '</td>'+
                                '<td>'+
                                    $('[name="end_date"]').val()+
                                '</td>'+
                                '<td>'+
                                    '<button type="button" name="update_event_btn" class="btn fasia-btn" id="'+response.ev_id+'"><i class="far fa-edit"></i></button>'+
                                    '<button type="button" name="delete_event_btn" class="btn fasia-btn" id="'+response.ev_id+'"><i class="fas fa-trash-alt"></i></button>'+
                                '</td>'+
                            '</tr>'
                        );
                    } else {
                        // updating the event in calender
                        var update_event = $("#calendar").fullCalendar('clientEvents', response.ev_id);
                        update_event[0].title = event_name;
                        update_event[0].start = start_date;
                        update_event[0].end = end_date;
                        update_event[0].description = event_description;
                        $('#calendar').fullCalendar('updateEvent', update_event[0]);
                        try {
                            // updating the event data in table list
                            $(event_name_td).html(event_name);
                            $(event_description_td).html(event_description);
                            $(start_date_td).html($('[name="start_date"]').val());
                            $(end_date_td).html($('[name="end_date"]').val());
                            event_name_td = '';
                            event_description_td = '';
                            start_date_td = '';
                            end_date_td = '';
                        } catch (error) {}
                    }
                    $('#admin_event_modal').modal('hide');
                    event_id = '';
                    $("[name='event_id']").val('');
                }
            },
            error: function(response) {
                alert('unable to add the event');
            }
        });
    }
});

// loading the list of events and showing in table
$("#list_events_link").on('click', function(e){
    $.ajax({
        type: 'GET',
        url:'/auth/admin-dashboard/admin_calendar/list',
        data:{},
        success: function(response){
            $("#calendar").hide();
            list_events_link.hide();
            $("#show_calendar_link").show();
            $("#list_calendar_div")
                .html(response)
                .show();
        },
        error: function(e){
            show_alert(
                'error', 
                '', 
                '<p>Unable to load events.<br /> Please try again after some time.</p>', 
                ''
            );
        }
    });
});

// function for toggle the calender and list events table
$("#show_calendar_link").on('click', function(e){
    $("#calendar").show();
    list_events_link.show();
    $("#show_calendar_link").hide();
    $("#list_calendar_div").hide();
});

// showing edit modal for update the event
$("#parent_calender_section").on('click', '[name="update_event_btn"]', function(e){
    var main_tr = $('#'+this.id).closest('tr')[0];
    event_name_td = main_tr.children[0];
    event_description_td = main_tr.children[1];
    start_date_td = main_tr.children[2];
    end_date_td = main_tr.children[3];
    $("input[name='event_id']").val(this.id);
    $("input[name='event_name']").val($(main_tr.children[0]).html());
    $("[name='event_description']").val($(main_tr.children[1]).html());
    $("input[name='start_date']").val($(main_tr.children[2]).html());
    $("input[name='end_date']").val($(main_tr.children[3]).html());
    submit_event_btn.html('UPDATE');
    show_bootstrap_modal('#admin_event_modal');
});

// Showing confirmation modal onclick of delete event button
$("#parent_calender_section").on('click', '[name="delete_event_btn"]', function(e){
    show_alert(
        'warning',
        '',
        '<p>Do you want to delete this event?</p>',
        'click:remove_event('+'"'+this.id+'"'+');'
    );
    $("#common_modal").find('#common_btn').html('Yes');
    $("#common_modal").find('.close').css('display', 'none');
    $('#common_modal').find('.modal-body').append(
        '<a class="btn common-model-btn" id="cal_no_btn" data-dismiss="modal" onclick="reset_cal_com_modal(this);">No</a>'
    );
});


// function for deleting the event from calender
function remove_event(id){
    $.ajax({
        method: 'DELETE',
        url: '/auth/admin-dashboard/calendar_event',
        data: {
            event_id: id
        },
        success: function (response) {
            if (response == 'success') {
                // removing event from calender
                $('#calendar').fullCalendar('removeEvents', [id]);
                // removing event from table list
                $('#'+id).closest('tr').remove();
                $("#common_modal").modal('hide');
            } else {
                alert('Unable delete the event.\n Please try again after some time.');
            }
        },
        error: function (e) {
            alert('Unable delete the event.\n Please try again after some time.');
        }
    });
}

// resetting the common modal after clicking no in delete confirmation modal
function reset_cal_com_modal(e){
    $(e).remove();
    $("#common_modal").find('#common_btn').html('Ok');
    $("#common_modal").find('.close').css('display', 'block');
    $("#common_modal").modal('hide');
}

// Resetting the modal fields on close of create/edit event modal
$("#admin_event_modal").on('hidden.bs.modal', function(e){
    $("form[name='event_form']")[0].reset();
});