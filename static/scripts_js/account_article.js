$(document).ready(function($){
	$('tr.class-body-row').click(function(){
		window.location = $(this).data("href");
	});
	$('button.class-edit-btn').click(function(e){
		e.stopPropagation();
		window.location = $(this).data("href");
	});
});

/* Sort table by columns */
var direction = [0, 0, 0];
$('th.class-header-title').click(function(){sortAlphaCol(0)});
$('th.class-header-type').click(function(){sortAlphaCol(1)});
$('th.class-header-date').click(function(){sortAlphaCol(2)});
function sortAlphaCol(column){
	var $rows, len=$('tr.class-body-row').length;
	let index;
	for(let i=0; i<len; i++){
		index = i;
		$rows = $('tr.class-body-row');
		for(let j=i+1; j<len; j++){
			if(direction[column] !== 1){
				if(column===2){
					if(compareDate($rows[index].cells[column].innerText, $rows[j].cells[column].innerText) === 1)
						index = j;
				}else if(column===1){
					if($($rows[index].cells[1]).data('sort') < $($rows[j].cells[1]).data('sort'))
						index= j;
				}else{
					if($rows[index].cells[column].innerText.toLowerCase() < $rows[j].cells[column].innerText.toLowerCase())
						index = j;			
				}
			}else{
				if(column===2){
					if(compareDate($rows[index].cells[column].innerText, $rows[j].cells[column].innerText) === -1)
						index = j;
				}else if(column===1){
					if($($rows[index].cells[1]).data('sort') > $($rows[j].cells[1]).data('sort'))
						index= j;
				}else{
					if($rows[index].cells[column].innerText.toLowerCase() > $rows[j].cells[column].innerText.toLowerCase())
						index = j;
				}
			}
		}
		$rows.eq(0).before($rows.eq(index));
	}
	if(direction[column] !== 1){
		direction = [0, 0, 0];
		direction[column] = 1;
	}else{
		direction = [0, 0, 0];
		direction[column] = -1
	}
	$('thead.class-table-header th i').attr('class', 'fas');
	if((direction[column] === 1 && column !== 2) || (direction[column] === -1 && column === 2)){
		$('thead.class-table-header th i').eq(column).addClass('fa-long-arrow-alt-up');
	}else{
		$('thead.class-table-header th i').eq(column).addClass('fa-long-arrow-alt-down');
	}
}

function compareDate(date1, date2){
	date1 = {
		day : Number(date1.substring(0,2)),
		month : Number(date1.substring(3,5)),
		year : Number(date1.substring(6,10))
	}
	date2 = {
		day : Number(date2.substring(0,2)),
		month : Number(date2.substring(3,5)),
		year : Number(date2.substring(6,10))
	}
	if(date1.year === date2.year){
		if(date1.month === date2.month){
			if(date1.day === date2.day)
				return 0;
			else if(date1.day > date2.day)
				return 1;
			else
				return -1;
		}else{
			if(date1.month > date2.month)
				return 1;
			else
				return -1;
		}
	}else{
		if(date1.year > date2.year)
			return 1;
		else
			return -1;
	}
}

/* Delete Articles */
var deletePopup = $('.class-delete-popup');
var posthide = $('input#delart');

function closeDeletePopup() {
	deletePopup.addClass('class-off');
}
$('.class-trash-btn').click(function(e){
	e.stopPropagation();
	deletePopup.removeClass('class-off');
	posthide.val($(this).parent().parent().data('id'));
});
$('.class-delete-cancel').add('.class-delete-times').click(function(){
	closeDeletePopup();
});

/* Search bar */
$('.class-accArt-searchbar').on('input', function(e) {
	let text = $(this).val().toLowerCase().trim();
	let emptyRow = $('tbody.class-table-body tr.class-body-empty');

	let rows = $('.class-body-accArt-row');
	let row;
	let visible_rows = 0;
	for (var i = rows.length - 1; i >= 0; i--) {
		row = rows.eq(i);

		if (row[0].cells[0].innerText.toLowerCase().includes(text)) {
			row.removeClass('class-off');
			visible_rows++;
		} else {
			row.addClass('class-off');
		}
	}
	if (visible_rows == 0) {
		emptyRow.removeClass('class-off');
	} else {
		emptyRow.addClass('class-off');
	}
});


/* Follow mechanic */
var icon = $('i.class-follow-fw-icon');
var span = $('.class-follow-fw-text');
$('button.class-follow-fw').hover(function(){
	icon.toggleClass("fa-check");
	span.text("Unfollow");
}, function(){
	icon.toggleClass("fa-check");
	span.text("Following");
});

/* Followers popup */
var follow_popup = $('.class-follow-popup');
$('.class-followers-btn').click(function(){
	follow_popup.removeClass('class-off');
	$('body').addClass('class-avoid-scroll');
});

function closeFollowPopup() {
	follow_popup.addClass('class-off');
	$('body').removeClass('class-avoid-scroll');
}
$('button.class-follow-cancel').add('i.class-follow-times').click(closeFollowPopup);

var tabFwer = $('.class-follow-tab-fwer');
var tabFwing = $('.class-follow-tab-fwing')
var follower = $('.class-follow-fwer');
var following = $('.class-follow-fwing');
function showFollower() {
	tabFwing.addClass('class-follow-tab-hidden');
	tabFwer.removeClass('class-follow-tab-hidden');
	following.addClass('class-off');
	follower.removeClass('class-off');
}
function showFollowing() {
	tabFwing.removeClass('class-follow-tab-hidden');
	tabFwer.addClass('class-follow-tab-hidden');
	following.removeClass('class-off');
	follower.addClass('class-off');
}
function resize(md) {
	if(md.matches){
		tabFwer.click(showFollower);
		tabFwing.click(showFollowing);
		showFollowing();
	}else{
		tabFwer.off();
		tabFwing.off();
		following.removeClass('class-off');
		follower.removeClass('class-off');
	}
}
var mediaQuery  = window.matchMedia("(max-width: 800px)");
resize(mediaQuery);
mediaQuery.addListener(resize);

$('i.class-follow-fwing-row-times').click(function(){
	$(this).parent().toggleClass('class-follow-fwing-row-selected');
});

var delfw = $('input#delfw');
function submitDelFw() {
	delfw.val('');
	let fw = $('.class-follow-fwing-row-selected');

	for (var i = 0; i < fw.length; i++) {
		delfw.val(delfw.val() + fw.eq(i).data('fwid') + ";;");
	}

	return (fw.length !== 0);
}

var windowEvent = function (event) {
	if(event.target == deletePopup[0]){
		closeDeletePopup();
	}else if(event.target == follow_popup[0]){
		closeFollowPopup();
	}
}
window.addEventListener('mousedown', windowEvent);