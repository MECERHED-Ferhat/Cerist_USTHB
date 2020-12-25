$('.main-container .delete-account .confirm-deletion button.cancel-deletion').click(function(){
    $('.main-container .delete-account .confirm-deletion').css('display','none');
    $('.main-container .delete-account .delete').css('display','initial');
});

$('.main-container .delete-account .delete button.alert').click(function(){
    $('.main-container .delete-account .delete').css('display','none');
    $('.main-container .delete-account .confirm-deletion').css('display','initial');
});