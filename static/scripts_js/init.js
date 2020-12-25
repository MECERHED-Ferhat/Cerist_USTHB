$('input#class-upload-input').removeAttr('required');
$('h1.class-wallpaper-welcome').css('left', '-100%');
$('img.class-wallpaper-documents').css('right', '-100%');
$(document).ready(function(){
	$('h1.class-wallpaper-welcome').delay(1000).animate({'left': '5%'}, 1500, 'swing');
	

	$('select').niceSelect();
	$('.class-slick').slick({
		infinite: false,
		slidesToShow: 4,
		slidesToScroll: 4,
		draggable: false,
		responsive: [
			{
				breakpoint: 1160,
				settings: {
					infinite: false,
					draggable: false,
					slidesToScroll: 3,
					slidesToShow: 3
				}
			},
			{
				breakpoint: 950,
				settings: {
					infinite: false,
					draggable: false,
					slidesToScroll: 2,
					slidesToShow: 2
				}
			},
			{
				breakpoint: 600,
				settings: {
					infinite: true,
					draggable: false,
					slidesToScroll: 1,
					slidesToShow: 1
				}
			}
		]
	});
});
function click_card(e){
	window.location = $(e).data("href");
}