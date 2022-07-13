$(document).ready(function() {
    //Set the carousel options
    $('#quote-carousel').carousel({
        pause: true,
        interval: 4000,
    });
    enable_or_disable_scroll_btn();
    //smooth scroll
    $(function() {
      $('.scroll').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
          if (target.length) {
            $('html, body').animate({
              scrollTop: target.offset().top - 69
            }, 800);
            return false;
          }
        }
      });
    });	
	
    
    // Clients carousel (uses the Owl Carousel library)
  // $(".clients-carousel").owlCarousel({
  //   autoplay: true,
  //   dots: true,
  //   loop: true,
  //   responsive: { 0: { items: 2 }, 768: { items: 4 }, 900: { items: 6 }
  //   }
  // });

  // // Testimonials carousel (uses the Owl Carousel library)
  // $(".testimonials-carousel").owlCarousel({
  //   autoplay: true,
  //   dots: true,
  //   loop: true,
  //   items: 1
  // });
    
});    

var $animation_elements = $('.animation-element');
var $window = $(window);

function check_if_in_view() {
  var window_height = $window.height();
  var window_top_position = $window.scrollTop();
  var window_bottom_position = (window_top_position + window_height);

  $.each($animation_elements, function() {
    var $element = $(this);
    var element_height = $element.outerHeight();
    var element_top_position = $element.offset().top;
    var element_bottom_position = (element_top_position + element_height);

    //check to see if this current container is within viewport
    if ((element_bottom_position >= window_top_position) &&
        (element_top_position <= window_bottom_position)) {
      $element.addClass('in-view');
    } else {
      $element.removeClass('in-view');
    }
  });
}

$window.on('scroll resize', check_if_in_view);
$window.trigger('scroll');

$(window).scroll(function() {
    enable_or_disable_scroll_btn();
});
$('.back-to-top').click(function(){
  $('html, body').animate({scrollTop : 0},1500, 'easeInOutExpo');
  return false;
});

function enable_or_disable_scroll_btn(){
  if ($(this).scrollTop() > 150) {
    $('.back-to-top').css('display', 'block');
  } else {
    $('.back-to-top').css('display', 'none');
  }
}

function show_search(id){
  if ($('#'+id).prop('checked') == true && id == 'radio_member'){
    $('#search_text').val('')
    $('#search_text').attr("placeholder", "Search by Email or Mobile");
  }
  else if ($('#'+id).prop('checked') == true && id == 'radio_chapter'){
    $('#search_text').val('')
    $('#search_text').attr("placeholder", "Search by Chapter");
  }
}

function get_data(){
  var search_type;
  var value = $('#search_text').val();
  if ($('#radio_member').prop('checked') == true)
    search_type = 'member';
  else if ($('#radio_chapter').prop('checked') == true)
    search_type = 'chapter';
  $.ajax({
    method: 'POST',
    url: '/search-member-chapter',
    beforeSend: setHeader,
    data: {
      search_value : value,
      search_type : search_type
    },
    success: function(response) {
      if(search_type == 'member')
        msg = '<p class="text-center">' +response.message+'</p>';
      else if(search_type == 'chapter')
        if(response.status == 'success')
          msg = '<p class="text-center">' +response.message+'. To know more click <a href="#"><font color="blue">'+value+'</font></a>.</p>';
        else
          msg = '<p class="text-center">' +response.message+'.</p>';
      show_alert(response.status, "", msg, '');
    }
  });
}

