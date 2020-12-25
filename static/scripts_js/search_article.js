/* Clickable rows */
$(document).ready(function($){
	$('tr.class-body-row').click(function(){
		window.location = $(this).data("href");
	});
	let date = new Date();
	let selectsFrom = $('.class-filter-select-from select');
	let selectsTo = $('.class-filter-select-to select');
	selectsFrom.eq(0).val(date.getDate());
	selectsTo.eq(0).val(date.getDate());
	selectsFrom.eq(1).val(date.getMonth()+1);
	selectsTo.eq(1).val(date.getMonth()+1);
	selectsFrom.eq(2).val(date.getFullYear());
	selectsTo.eq(2).val(date.getFullYear());
});

/* Filter button */
$('button.class-filter-btn').click(function(){
	$('form.class-filter-content').slideToggle();
	$('i.class-filter-btn-icon').toggleClass('class-rotate-arrow');
});

function validateFilterSearch(e){
	return ($('input#class-filter-input-title').val().search(/[A-zÀ-ú0-9-]+/) >= 0 ||
			$('input#class-filter-input-author').val().search(/[A-zÀ-ú0-9-]+/) >= 0 ||
			$('select#class-filter-input-doctype').val() < 4 ||
			$('.class-filter-select-from').css('display') !== 'none' ||
			$('.class-filter-select-to').css('display') !== 'none');
}

/* Date filter buttons */
var toggleFrom = false;
var toggleTo = false;
 
$('.class-filter-drop-from').click(function(){
	$('.class-filter-select-from').slideToggle();
	$('i.class-filter-icon-from').toggleClass('class-rotate-arrow');
	if(toggleFrom){
		$('.class-filter-select-from select').attr('name', 'filter-from-none');
	}else{
		$('select#class-filter-select-from-day').attr('name', 'filter-from-day');
		$('select#class-filter-select-from-month').attr('name', 'filter-from-month');
		$('select#class-filter-select-from-year').attr('name', 'filter-from-year');
	}
	toggleFrom = !toggleFrom;
});
$('.class-filter-drop-to').click(function(){
	$('.class-filter-select-to').slideToggle();
	$('i.class-filter-icon-to').toggleClass('class-rotate-arrow');
	if(toggleTo){
		$('.class-filter-select-to select').attr('name', 'filter-to-none');
	}else{
		$('select#class-filter-select-to-day').attr('name', 'filter-to-day');
		$('select#class-filter-select-to-month').attr('name', 'filter-to-month');
		$('select#class-filter-select-to-year').attr('name', 'filter-to-year');
	}
	toggleTo = !toggleTo;
});

/* Sort table by columns */
var direction = [0, 0, 0, 0];
$('th.class-header-title').click(function(){sortAlphaCol(0)});
$('th.class-header-author').click(function(){sortAlphaCol(1)});
$('th.class-header-type').click(function(){sortAlphaCol(2)});
$('th.class-header-date').click(function(){sortAlphaCol(3)});
function sortAlphaCol(column){
	var $rows, len=$('tr.class-body-row').length;
	let index;
	for(let i=0; i<len; i++){
		index = i;
		$rows = $('tr.class-body-row');
		for(let j=i+1; j<len; j++){
			if(direction[column] !== 1){
				if(column===3){
					if(compareDate($rows[index].cells[column].innerText, $rows[j].cells[column].innerText) === 1)
						index = j;
				}else if(column===2){
					if($($rows[index].cells[2]).data('sort') < $($rows[j].cells[2]).data('sort'))
						index= j;
				}else{
					if($rows[index].cells[column].innerText.toLowerCase() < $rows[j].cells[column].innerText.toLowerCase())
						index = j;			
				}
			}else{
				if(column===3){
					if(compareDate($rows[index].cells[column].innerText, $rows[j].cells[column].innerText) === -1)
						index = j;
				}else if(column===2){
					if($($rows[index].cells[2]).data('sort') > $($rows[j].cells[2]).data('sort'))
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
		direction = [0, 0, 0, 0];
		direction[column] = 1;
	}else{
		direction = [0, 0, 0, 0];
		direction[column] = -1
	}
	$('thead.class-table-header th i').attr('class', 'fas');
	if((direction[column] === 1 && column !== 3) || (direction[column] === -1 && column === 3)){
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