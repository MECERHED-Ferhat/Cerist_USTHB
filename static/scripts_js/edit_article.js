var area_conference = $('.class-form-conference');
var area_rn = $('.class-form-rn');
var area_report = $('.class-form-report');
var input_doctype = $('select#id_doctype');

function changeDocType() {
	area_conference.addClass('class-off');
	area_rn.addClass('class-off');
	area_report.addClass('class-off');

	if (input_doctype.val() === '1')
		area_conference.removeClass('class-off');
	else if (input_doctype.val() === '2')
		area_rn.removeClass('class-off');
	else if (input_doctype.val() === '3')
		area_report.removeClass('class-off');
}

$(document).ready(function() {
	$('.class-tags-bubbles span.class-tags-bubbles-entity').hover(onCross, offCross).click(rmTag);
	$('.class-author-bubbles span.class-author-bubbles-entity').hover(onCrossA, offCrossA).click(rmAuthor);

	let date_input = $('#class-conf-date-input');
	let pages_input = $('#class-rn-pages-input');
	let date_regex = date_input.val().match(/^(\d{4})-(\d{2})-(\d{2})$/);
	let pages_regex = pages_input.val().match(/^pp (\d+)-(\d+)$/);
	if (date_regex !== null) {
		let selects = $('.class-conf-date-container select');
		selects.eq(0).val(Number(date_regex[3]));
		selects.eq(1).val(Number(date_regex[2]));
		selects.eq(2).val(Number(date_regex[1]));
	} else if (pages_regex !== null) {
		$('#class-rn-pages-input-start').val(pages_regex[1]);
		$('#class-rn-pages-input-end').val(pages_regex[2]);
	}
	date_input.val('');
	pages_input.val('');

	changeDocType();
	input_doctype.on('change', changeDocType);

	reconstructAuthors();
	reconstructTags();
});


/* ------BB Tab tags------ */
function reconstructTags() {
	let vf = $('input#class-tags-input-field');
	let hf = $('.class-tags-input-hidden');
	let words = hf.val().split(';;');

	for (var i = words.length - 1; i >= 0; i--) {
		vf.val(words[i]);
		addTag();
	}

	hf.val('');
}

$('input#class-tags-input-field').focusin(function(){
	$('.class-tags-container').toggleClass('class-bbtab-container-highlight');
		}).focusout(function(){
	$('.class-tags-container').toggleClass('class-bbtab-container-highlight');
});

var rm = $('.class-tags-bubbles-cross');

function offCross(){
	rm.addClass('class-off');
	rm.css('opacity', '0');
}
function onCross(){
	$(this).append(rm);
	rm.removeClass('class-off');
	rm.animate({'opacity':'.9'}, 300, 'swing');
}
$('span.class-tags-bubbles-entity').hover(onCross, offCross);

function rmTag(){
	offCross();
	$('.class-form-tags').append(rm);
	$(this).remove();
}
$('span.class-tags-bubbles-entity').click(rmTag);

function addTag(){
	let $field = $('input#class-tags-input-field');
	let $error = $('span.class-tags-error');
	let field_content = $field.val();
	field_content = field_content.trim().replace(/\s+/g, ' ');
	if(field_content === ''){

	}else if($('.class-tags-bubbles .class-tags-bubbles-entity').length >= 10){
		$error.text('*Tags are limited to 10 per article');
		if($error.css('display') === 'none')
			$error.fadeIn(300).delay(3000).fadeOut(1000);
	}else if(field_content.length > 32){
		$error.text('*Tag must have at most 32 characters');
		if($error.css('display') === 'none')
			$error.fadeIn(300).delay(3000).fadeOut(1000);
	}else if(field_content.search(/^(\s)*[A-zÀ-ú0-9'_-]+([A-zÀ-ú0-9'_-]|\s)*$/) < 0){
		$error.text('*Tags can only contain alphanumeric characters');
		if($error.css('display') === 'none')
			$error.fadeIn(300).delay(3000).fadeOut(1000);
	}else{
		$('.class-tags-bubbles').append('<span class="class-bbtab-bubbles-entity class-tags-bubbles-entity hyphenate">'+ field_content +'</span>');
		$field.val('');
		$('.class-tags-bubbles span.class-tags-bubbles-entity:last-child').hover(onCross, offCross).click(rmTag);
	}
}
$('i.class-tags-input-icon').click(addTag);
$('input#class-tags-input-field').keypress(function(e){
	if(e.which === 13){
		addTag();
		e.preventDefault();
		return false;
	}
});

function makeTags() {
	let hidden_field = $('input.class-tags-input-hidden');
	hidden_field.val('');
	[...$('span.class-tags-bubbles-entity')].forEach(bubble => {
		hidden_field.val(hidden_field.val() + $(bubble).text() + ';;');
	});
}
/* ------------------ */

/* --BB Tab Authors-- */
function reconstructAuthors() {
	let vf = $('input#class-author-input-field');
	let hf = $('.class-author-input-hidden');
	let words = hf.val().split(';;');

	for (var i = words.length - 1; i >= 0; i--) {
		vf.val(words[i].split('$$')[1]);
		addAuthor();
	}

	hf.val('');
}
$('input#class-author-input-field').focusin(function(){
	$('.class-author-container').toggleClass('class-bbtab-container-highlight');
		}).focusout(function(){
	$('.class-author-container').toggleClass('class-bbtab-container-highlight');
});

var rma = $('.class-author-bubbles-cross');

function offCrossA(){
	rma.addClass('class-off');
	rma.css('opacity', '0');
}
function onCrossA(){
	$(this).append(rma);
	rma.removeClass('class-off');
	rma.animate({'opacity':'.9'}, 300, 'swing');
}
$('span.class-author-bubbles-entity').hover(onCrossA, offCrossA);

function rmAuthor(){
	offCrossA();
	$('.class-form-author').append(rma);
	$(this).remove();
}
$('span.class-author-bubbles-entity').click(rmAuthor);

function addAuthor(){
	let id_value = 0, current_row;
	let $field = $('input#class-author-input-field');
	let $error = $('span.class-author-error');
	let field_content = $field.val();
	field_content = field_content.trim().replace(/\s+/g, ' ');
	if(field_content === ''){

	}else if($('.class-author-bubbles .class-author-bubbles-entity').length >= 8){
		$error.text('*There can be at most 8 authors per article');
		if($error.css('display') === 'none')
			$error.fadeIn(300).delay(3000).fadeOut(1000);
	}else if(field_content.length > 181){
		$error.text('*Author name cannot exceed 40 characters');
		if($error.css('display') === 'none')
			$error.fadeIn(300).delay(3000).fadeOut(1000);
	}else if(field_content.search(/^(\s)*[A-zÀ-ú0-9-]+([A-zÀ-ú0-9'_-]|\s)*$/) < 0){
		$error.text('*Author name can only contain alphanumeric characters');
		if($error.css('display') === 'none')
			$error.fadeIn(300).delay(3000).fadeOut(1000);
	}else{
		for (var i = array_accounts.length - 1; i >= 0; i--) {
			current_row = array_accounts.eq(i)
			if (current_row.data('ln') + ' ' + current_row.data('fn') === field_content) {
				id_value = current_row.data('id');
				break;
			}
		}
		$('.class-author-bubbles').append('<span data-id="'+ id_value +'" class="class-bbtab-bubbles-entity class-author-bubbles-entity hyphenate">'+ field_content +'</span>');
		$field.val('');
		$('.class-author-bubbles span.class-author-bubbles-entity:last-child').hover(onCrossA, offCrossA).click(rmAuthor);
	}
}
var author_addBtn = $('i.class-author-input-icon');
author_addBtn.click(addAuthor);
$('input#class-author-input-field').keypress(function(e){
	if(e.which === 13){
		addAuthor();
		e.preventDefault();
		return false;
	}	
});

function makeAuthor() {
	let hidden_field = $('input.class-author-input-hidden');
	hidden_field.val('');
	[...$('span.class-author-bubbles-entity')].forEach(bubble => {
		hidden_field.val(hidden_field.val() + $(bubble).data('id') + '$$' + $(bubble).text().trim() + ';;');
	});
}
/* ------------------ */

/* post traintement extra info article */
function makeDate() {
	let date = $('.class-conf-date-container select');
	$('input#class-conf-date-input').val(date.eq(2).val() + '-' + date.eq(1).val() + '-' + date.eq(0).val());
}
function makePages() {
	let pages_start = $('input#class-rn-pages-input-start');
	let pages_end = $('input#class-rn-pages-input-end');
	$('input#class-rn-pages-input').val(pages_start.val() + '-' + pages_end.val());
}

/* ------------------ */

/* Authors auto-complete */
var display_accounts = $('.class-author-list');
var array_accounts = $('.class-author-entity');
var author_input = $('input#class-author-input-field');

var current_focus = -1;
function authorAuto() {
	let val = $(this).val();
	if (!val) {
		display_accounts.addClass('class-off');
		return false;
	}
	let empty = true;
	current_focus = -1;

	for (var i = array_accounts.length - 1; i >= 0; i--) {
		let current_row = array_accounts.eq(i);
		let full_name = current_row.data('ln') + ' ' + current_row.data('fn');

		current_row.removeClass('class-author-entity-selected');
		if (current_row.data('ln').substr(0, val.length).toUpperCase() === val.toUpperCase()) {
			empty = false;
			current_row.removeClass('class-off');
			current_row[0].lastElementChild.innerHTML = '<strong>' + current_row.data('ln').substr(0, val.length) + '</strong>';
			current_row[0].lastElementChild.innerHTML += current_row.data('ln').substr(val.length);
			current_row[0].lastElementChild.innerHTML += ' ' + current_row.data('fn');
		} else if (current_row.data('fn').substr(0, val.length).toUpperCase() === val.toUpperCase()) {
			empty = false;
			current_row.removeClass('class-off');
			current_row[0].lastElementChild.innerHTML = current_row.data('ln');
			current_row[0].lastElementChild.innerHTML += ' <strong>' + current_row.data('fn').substr(0, val.length) + '</strong>';
			current_row[0].lastElementChild.innerHTML += current_row.data('fn').substr(val.length);
		} else if (full_name.substr(0, val.length).toUpperCase() === val.toUpperCase()) {
			empty = false;
			current_row.removeClass('class-off');
			current_row[0].lastElementChild.innerHTML = '<strong>' + full_name.substr(0, val.length) + '</strong>' + full_name.substr(val.length);
		} else {
			current_row.addClass('class-off');
		}
	}
	if (empty) 
		display_accounts.addClass('class-off');
	else
		display_accounts.removeClass('class-off');
}
function authorKeyPress(e) {
	if (display_accounts.hasClass('class-off')) return true;

	let active_rows = $('.class-author-entity:not(.class-off)');
	if (active_rows.length === 0) return true;

	if (e.keyCode === 40 || e.keyCode === 9) {		// Arrow down
		e.preventDefault();
		if (current_focus >= 0 && current_focus < active_rows.length)
			active_rows.eq(current_focus).removeClass('class-author-entity-selected');

		current_focus++;
		if (current_focus >= active_rows.length) current_focus = 0;

		active_rows.eq(current_focus).addClass('class-author-entity-selected');		
	} else if (e.keyCode === 38) {		// Arrow Up
		if (current_focus >= 0 && current_focus < active_rows.length)
			active_rows.eq(current_focus).removeClass('class-author-entity-selected');

		current_focus--;
		if (current_focus < 0) current_focus = active_rows.length - 1;

		active_rows.eq(current_focus).addClass('class-author-entity-selected');
	} else if (e.keyCode === 13) {
		e.preventDefault();

		if (current_focus > -1)
			active_rows[current_focus].click();
	}
}
author_input.on('input', authorAuto);
author_input.on('keydown', authorKeyPress);

array_accounts.click(function() {
	author_input.val($(this).data('ln') + ' ' + $(this).data('fn'));
	author_addBtn[0].click();
	display_accounts.addClass('class-off');
});

document.addEventListener("click", function (e) {
    display_accounts.addClass('class-off');
});
/* --------------------- */