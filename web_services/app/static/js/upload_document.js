function upload_document(form_id){
    var form_data = new FormData($('#' + form_id)[0]);
    return $.ajax({
        type: 'POST',
        url: '/upload_file',
        beforeSend: setHeader,
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: true
    });
}

function attach_document(element_id, data, remove_fun){
    var r = $.Deferred();
    var download = document.getElementById(element_id);
    var child_div = document.createElement('div');
    // creating text p tag
    var attach_text = document.createElement('p');
    attach_text.setAttribute('class', 'attach_classs');
    attach_text.innerHTML = 'Attached';
    // creating download element
    var download_file = document.createElement('a');
    download_file.setAttribute('href', data.url);
    download_file.setAttribute('class', 'download_link_color');
    download_file.setAttribute('onclick', "window.open('" + data + "', 'newwindow', 'toolbar=yes,scrollbars=yes,resizable=yes,top=250,left=500,width=550, height=550'); return false;");
    download_file.innerHTML = "<i class='fa fa-eye' aria-hidden='true'></i>";
    // creating delete button tag
    var remove_file = document.createElement('a');
    remove_file.innerHTML = "<i class='glyphicon glyphicon-trash download_link_color'></i>";
    remove_file.setAttribute("onclick", remove_fun+"('"+data+"'"+","+"this"+");");
    // appending all tags to main div
    child_div.appendChild(attach_text);
    child_div.appendChild(download_file);
    child_div.appendChild(remove_file);
    var break_tag = document.createElement('br');
    child_div.appendChild(break_tag);
    download.appendChild(child_div);
    return r;
}