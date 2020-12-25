from django import forms
from . import models
from django.core.exceptions import ValidationError
from project.settings import MAX_UPLOAD
import re, datetime

class TagForm(forms.Form):

	tags = forms.CharField(widget=forms.HiddenInput(attrs={'class' : 'class-tags-input-hidden'}),
						   required=False)

	def clean_tags(self):
		data = self.cleaned_data['tags'].strip()
		if data == '':
			return []
		elif(re.match(r"^([\w\s' _-]{1,32};;){0,10}$", data, re.UNICODE)):
			return list(set(re.split(' *;; *', data[:len(data)-2])))
		else:
			raise ValidationError('These tags cannot be applied')

class AuthorForm(forms.Form):

	use_required_attribute = False

	authors = forms.CharField(widget=forms.HiddenInput(attrs={'class' : 'class-author-input-hidden'}),
							  required=True)
	authors.error_messages['required'] = ('At least one author is required')

	def clean_authors(self):
		data = re.sub(r'\s+', ' ', self.cleaned_data['authors'].strip())
		if data == '':
			raise ValidationError('At least one author is required');
		elif(re.match(r"^(\d+\$\$[\w\s' _-]{1,180};;){0,8}$", data, re.UNICODE)):
			unite = list(set(re.split(' *;; *', data[:len(data)-2])))
			retour = []
			for x in unite:
				retour.append(x.split('$$'))
				retour[-1][0] = int(retour[-1][0])
			return retour
		else:
			raise ValidationError('These author names cannot be applied')



class ConferenceForm(forms.ModelForm):

	use_required_attribute = False


	name_conference = forms.CharField(widget=forms.TextInput(attrs={'id':'class-conf-name-input',
															 'class':'class-textfield'}))
	editor_conference = forms.CharField(widget=forms.TextInput(attrs={'id':'class-conf-editor-input',
														   'class':'class-textfield'}))
	audience_conference = forms.IntegerField(widget=forms.RadioSelect(attrs={'id':'class-conf-audience-input'},
														   choices=models.AUDIENCE))
	reading_committee_conference = forms.IntegerField(widget=forms.RadioSelect(attrs={'id':'class-conf-read-input'},
																			   choices=models.YES_NO))
	location_conference = forms.CharField(widget=forms.TextInput(attrs={'id':'class-conf-loc-input',
																		'class':'class-textfield'}))
	procedding = forms.IntegerField(widget=forms.RadioSelect(attrs={'id':'class-conf-proc-input'},
															 choices=models.YES_NO))

	date_conference = forms.DateField(widget=forms.HiddenInput(attrs={'id':'class-conf-date-input'}))

	class Meta:
		model = models.Conference
		fields = ['name_conference', 'editor_conference', 'audience_conference', 'reading_committee_conference', 'location_conference', 'procedding', 'date_conference']


class ReviewNewsForm(forms.ModelForm):

	def clean_pages(self):
		data = self.cleaned_data['pages'].strip().split('-')
		
		if len(data) == 2 and data[0].isnumeric() and data[1].isnumeric():
			if int(data[0]) < int(data[1]):
				return 'pp ' + self.cleaned_data['pages']
			else:
				raise ValidationError('Inconsistent date interval')
		else:
			return None

	use_required_attribute = False

	name_RN = forms.CharField(widget=forms.TextInput(attrs={'id':'class-rn-name-input',
														     'class':'class-textfield'}))
	editor_RN = forms.CharField(widget=forms.TextInput(attrs={'id':'class-rn-editor-input',
														   'class':'class-textfield'}))
	audience_RN = forms.IntegerField(widget=forms.RadioSelect(attrs={'id':'class-rn-audience-input'},
														   choices=models.AUDIENCE))
	reading_committee_RN = forms.IntegerField(widget=forms.RadioSelect(attrs={'id':'class-rn-read-input'},
																			   choices=models.YES_NO))
	type_RN = forms.IntegerField(widget=forms.RadioSelect(attrs={'id':'class-rn-type-input'},
														  choices=models.TYPE_RN))

	pages = forms.CharField(widget=forms.HiddenInput(attrs={'id':'class-rn-pages-input'}))

	class Meta:
		model = models.ReviewNews
		fields = ['name_RN', 'editor_RN', 'audience_RN', 'reading_committee_RN', 'type_RN', 'pages']


class ReportForm(forms.ModelForm):

	use_required_attribute = False

	type_RP = forms.IntegerField(widget=forms.Select(attrs={'id':'class-report-type-input',
															'class':'wide'},
													 choices=models.TYPE_RP))

	num_report = forms.CharField(widget=forms.TextInput(attrs={'id':'class-report-num-input',
															   'class':'class-textfield'}))

	class Meta:
		model = models.Report
		fields = ['type_RP', 'num_report']


class ArticleForm(forms.ModelForm):

	def clean_document(self):
		value = self.cleaned_data['document']

		if self.instance is not None:
			return value

		if value.content_type != 'application/pdf':
			raise ValidationError('Only .PDF files are accepted')
		if value.size > MAX_UPLOAD:
			raise ValidationError('File size should be under:%(MAX)s. Current file size:%(SIZE)s',
								  params={'MAX':filesizeformat(MAX_UPLOAD), 'SIZE':filesizeformat(value.size)})

		return value

	def clean_title(self):
		data = re.sub(r'\s+', ' ', self.cleaned_data['title'].strip())
		if re.search(r'\w+', data, re.UNICODE):
			return data
		else:
			raise ValidationError('This title contain no alphabetic character')

	document = forms.FileField(widget=forms.FileInput(attrs={'id' : 'class-upload-input',
															 'onchange' : 'handleFiles(this.files)',
															 'accept' : '.pdf'}),
							   required=True,
							   allow_empty_file=False)
	document.error_messages['required'] = ('File upload is required')
	document.error_messages['empty'] = ('Uploaded file is empty')
	document.error_messages['invalid'] = ('Uploaded file is invalid')

	title = forms.CharField(widget=forms.TextInput(attrs={'id' : 'class-title-input',
														  'class' : 'class-textfield'}),
												   required=True)
	title.error_messages['required'] = ('Title is required')

	summary = forms.CharField(widget=forms.Textarea(attrs={'class' : 'class-summary-textarea class-textfield',
															'rows' : 20,
															'style' : 'height : auto;'}),
													required=False)

	class Meta:
		model = models.Article
		fields = ['document', 'title', 'doctype', 'summary']
		widgets = {
			'doctype' : forms.Select(attrs={'class' : 'wide'},
									 choices=models.DOCTYPE_CHOICES)
		}