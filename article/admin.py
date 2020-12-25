from django.contrib import admin
from article import models

class TagInline(admin.StackedInline):
	model = models.Tag
	extra = 0
	max_num = 10

class AuthorInline(admin.StackedInline):
	model = models.Author
	extra = 0
	max_num = 8

class ConferenceInline(admin.StackedInline):
	model = models.Conference
	extra = 0

class ReviewNewsInline(admin.StackedInline):
	model = models.ReviewNews
	extra = 0

class ReportInline(admin.StackedInline):
	model = models.Report
	extra = 0

class ArticleAdmin(admin.ModelAdmin):
	inlines = [
		AuthorInline,
		ConferenceInline,
		ReviewNewsInline,
		ReportInline,
		TagInline,
	]
	fields = [
		'title',
		'postmaster',
		'document',
		'summary',
		'rdf'
	]
	list_display = ('title', 'postmaster', 'document_type')

	def document_type(self, obj):
		for i in models.DOCTYPE_CHOICES:
			if i[0] == str(obj.doctype):
				return i[1]
		return ""

admin.site.register(models.Article, ArticleAdmin)