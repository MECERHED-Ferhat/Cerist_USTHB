
$(document).ready(function(e){
	
	$('.class-collapse-content').slideToggle();
	$('div.toggle-menu').css('display', 'block');
	

	$('.class-log-menu').slideToggle();
	$('.class-log-menu-container').css('display', 'block');

});

window.onresize = function(event) {
	if ( Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 700)
	{	
		$('div.toggle-menu').css('display', 'none');
		$('.class-collapse-content').slideUp();
		
	}
	else
	{
		$('div.toggle-menu').css('display', 'block');
	}
    
};


$('button.class-collapse-btn').click(function(e){
	$('.class-collapse-content').slideToggle();
});

$('.class-navbar-log').click(function(e){
	$('.class-log-menu').slideToggle();
});

function validateSearchBar(e) {
	return ($('input.class-search-bar').val().search(/[A-zÀ-ú0-9-]+/) >= 0);
}