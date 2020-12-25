var table = $('table.class-notif-table');
var checkboxs = $('td.class-notif-check input');
var all_btn = $('th.class-notif-col-all span');
var del_btn = $('th.class-notif-col-del button');
var hid_field = $('input.class-notif-hid');
var checkedboxs = 0;

$(document).ready(function() {
	for (let i = 0; i < checkboxs.length; i++) {
		checkboxs[i].checked = false;
	}
});



function activateDelete() {
	if (checkedboxs > 0) {
		del_btn.addClass('class-notif-clickable');
		del_btn.attr('type', 'submit');
	} else {
		del_btn.removeClass('class-notif-clickable');
		del_btn.attr('type', 'button');
	}
}

all_btn.click(function() {
	if (checkedboxs < checkboxs.length){
		for (let i = 0; i < checkboxs.length; i++){
			if(!checkboxs[i].checked){
				checkboxs[i].checked = true;
			}
		}
		checkedboxs = checkboxs.length;
	}else{
		for (let i = 0; i < checkboxs.length; i++){
			if(checkboxs[i].checked){
				checkboxs[i].checked = false;
				checkedboxs--;
			}
		}
		checkedboxs = 0;
	}
	activateDelete();
});

checkboxs.change(function() {
	if (this.checked) {
		checkedboxs++;
	} else {
		checkedboxs--;
	}
	activateDelete();
});

function submitDelNot(e) {
	hid_field.val('');
	if (checkedboxs > 0){
		let id;
		for (let i = 0; i < checkboxs.length; i++){
			if (checkboxs[i].checked) {
				id = checkboxs.eq(i).parent().parent().data('id');
				if (Number.isInteger(id))
					hid_field.val(hid_field.val() + id + ';;');
				else
					return false;
			}
		}
		return (hid_field !== '');
	} else {
		return false;
	}
}