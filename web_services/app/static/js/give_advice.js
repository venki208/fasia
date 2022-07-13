var give_advice_btn = $("button[name='give_advice']");
var submit_advice_btn = $("button[name='advice_button']");
var view_advice_answer_btn = $("button[name='view_advice_answer_btn']");
var submit_search_btn = $('#search_btn');
var search_data = [];
var is_match_string = false;
var arr_val;

// Showing give advice modal
give_advice_btn.on('click', function(e){
	$("[name='advice_id']").val($(this).attr('g_adv_id'));
	show_bootstrap_modal('#giveAdvisorModal');
});

// uploading documents and adding response value to input
$("#give_advice_document").on('change', function(e){
	if($(this).val() != ''){
        var up_document = upload_document('give_advice_doc');
        up_document.success(function(response){
            var doc_urls = $("[name='give_advice_doc_urls']").val();
            if (doc_urls){
                doc_urls = doc_urls+","+response;
                $("[name='give_advice_doc_urls']").val(doc_urls);
            }else{
				$("[name='give_advice_doc_urls']").val(response);
            }
			attach_document('give_advice_uploaded_docs', response, 'remove_give_advice_doc')
				.done(hide_show_upload_btn("[name='give_advice_doc_urls']", "#paper_clip1"));
        });
        up_document.error(function(response){
            alert('unable to upload');
        });
    }
});

// removing documents
function remove_give_advice_doc(url, event){
    var doc_urls = $("[name='give_advice_doc_urls']").val();
    var doc_urls_array = doc_urls.split(',');
    for (i=0; i<doc_urls_array.length; i++){
        if(doc_urls_array[i] == url){
            doc_urls_array.splice(i, 1);
        }
    }
    $("[name='give_advice_doc_urls']").val(doc_urls_array.join());
	$(event).parent().remove();
	hide_show_upload_btn("[name='give_advice_doc_urls']", "#paper_clip1");
}

// submitting the advice answer
submit_advice_btn.on('click', function(e){
	$.ajax({
		method: 'POST',
		url: '/advice/give-advice',
		beforeSend: setHeader,
		data: {
			'advice_id': $('[name="advice_id"]').val(),
			'doc_urls': $('[name="give_advice_doc_urls"]').val(),
			'answer': $('[name="give_advice_answer"]').val()
		},
		success: function(response){
			if(response == 'success'){
				$("#give_advice_uploaded_docs").empty();
				$("#give_advice_form")[0].reset();
				show_alert(
					'success',
					'giveAdvisorModal',
					'<p>Thanks for your help. Your recommendation is highly appreciated. FASIA will communicate with the advice seeker.</p>',
					'reload: true'
				);
			}
		},
		error: function(response){
			alert('Unable to process your request \n Please try again after some time');
		}
	});
});

// Listing the answers of advice question
view_advice_answer_btn.on('click', function(e){
	$.ajax({
		method: 'POST',
		url: '/advice/get-advice-answer',
		beforeSend: setHeader,
		data:{
			'advice_id': $(this).attr('g_adv_id')
		},
		success: function(response){
			$("#advice_list_common_modal_div").html();
			$("#advice_list_common_modal_div").html(response);
			show_bootstrap_modal('#listAnswerModal');
		},
		error: function(response){
			alert('Unable to load answers \n Please try again after some time');
		}
	});
});

// Seach functionality for advice
$("input#search_answers").autocomplete({
	source: function (request, response) {
		$('input[name="search_question_id"]').val('');
		for(arr_val in search_data){
			if (search_data[arr_val].label.indexOf(request.term) >= 0){
				is_match_string = true;
				break;
			}else{
				is_match_string = false;
			}
		}
		if (is_match_string){
			response(search_data);
		}else{
			$.ajax({
				dataType: "json",
				type: 'POST',
				url: '/advice/search-advice',
				beforeSend: setHeader,
				data: {
					s_key: $('#search_answers').val()
				},
				success: function (data) {
					search_data = [];
					search_data = $.map(data.advices, function (item) {
						return search_data.concat({ label: item.title, value: item._id.$oid});
					});
					response(search_data);
				},
				error: function (data) {

				}
			});
		}
	},
	minLength: 3,
	autoFocus: true,
	select: function (event, ui) {
		event.preventDefault();
		$(this).val(ui.item.label);
		$('input[name="search_question_id"]').val(ui.item.value);
		search_data = [];
	}
});

submit_search_btn.on('click', function(e){
	$("[name='search_form']").submit();
});
