var profile_pic = $('#id_profile_pic');
var img_btn = $('label.class-profile-pic-label')
profile_pic.change(changeImage);
function changeImage() {
	if (this.files && this.files[0]) {
		if (this.files[0].type.match(/^image\//)) {
			let imageToProcess = this.files[0];
			img_btn.text(imageToProcess.name);
		}
	}
}