from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, FileResponse
from django.db.models import Q
from . import forms
from . import models
from account.models import Account
from project.settings import MEDIA_ROOT
import os, re
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.decorators import unauthenticated_user

SELECT_DAY = [x for x in range(1,32)]
SELECT_MONTH = [x for x in range(1,13)]
SELECT_YEAR = [x for x in range(2015, 2040)]


@login_required(login_url="home:login")
def addArticle(request):
	context = {'SELECT_DAYS' : [SELECT_DAY, SELECT_MONTH, SELECT_YEAR]}
	context['accounts'] = Account.objects.all()
	profile = request.user.account

	if request.method == 'POST':
		formArticle = forms.ArticleForm(request.POST or None, request.FILES or None)
		formTag = forms.TagForm(request.POST or None)
		formAuthor = forms.AuthorForm(request.POST or None)
		context['form_conference'] = forms.ConferenceForm()
		context['form_reviewNews'] = forms.ReviewNewsForm()
		context['form_report'] = forms.ReportForm()
		
		dt = str(request.POST['doctype'])
		formExtraInfo = None
		if dt == '1':
			formExtraInfo = forms.ConferenceForm(request.POST or None)
			context['form_conference'] = formExtraInfo
		elif dt == '2':
			formExtraInfo = forms.ReviewNewsForm(request.POST or None)
			context['form_reviewNews'] = formExtraInfo
		elif dt == '3':
			formExtraInfo = forms.ReportForm(request.POST or None)
			context['form_report'] = formExtraInfo

		if formArticle.is_valid() and \
		   formTag.is_valid() and \
		   formAuthor.is_valid() and \
		   (formExtraInfo is None or formExtraInfo.is_valid()):

			# Create new article
			art = formArticle.save(commit=True)

			# Link extra info
			if not formExtraInfo is None:
				fei = formExtraInfo.save(commit=False)
				fei.article = art
				fei.save()

			# Create tags
			for bubble in formTag.cleaned_data['tags']:
				tag = models.Tag(tag_name = bubble, tag_article = art)
				tag.save()

			# Create authors (['id', 'full_name'])
			for bubble in formAuthor.cleaned_data['authors']:
				author = models.Author(author_name = bubble[1], user_ref = None, article_ref = art)

				if bubble[0] > 0:
					try:
						user = Account.objects.get(id=bubble[0])
					except Exception as e:
						pass
					else:
						author.user_ref = user

						# Create notification for identified authors
						if user != profile:
							notif = models.Notification(source = profile, destination = user, topic = art, notif_type = 0)
							notif.save()
							user.new_notifications = True
							user.save()

				author.save()

			# Link to postmaster
			profile.article_set.add(art)

			# Create RDF
			art.create_rdf(request)

			# Create notification for followers
			for acc in profile.account_set.all():
				notif = models.Notification(source = profile, destination = acc, topic = art, notif_type = 1)
				notif.save()
				acc.new_notifications = True
				acc.save()

			return redirect('/article/read/' + str(art.id))

		else:
			context['form'] = formArticle
			context['form_tag'] = formTag
			context['form_tag_errors'] = formTag['tags'].errors
			context['form_author'] = formAuthor
			context['form_author_errors'] = formAuthor['authors'].errors

			return render(request, 'accounts/ajout_article.html', context)

	context['form_author'] = forms.AuthorForm()
	context['form_tag'] = forms.TagForm()
	context['form_conference'] = forms.ConferenceForm()
	context['form_reviewNews'] = forms.ReviewNewsForm()
	context['form_report'] = forms.ReportForm()
	context['form'] = forms.ArticleForm()
	return render(request, 'accounts/ajout_article.html', context)


def readArticle(request, id):
	context = {}
	context['authors_read'] = []
	context['art'] = get_object_or_404(models.Article, id=id)
	context['color'] = 'header-'+str(context['art'].doctype)
	context['art_tags'] = context['art'].tag_set.all().values()
	context['authors_read'] = context['art'].author_set.all()

	return render(request, 'read_article.html', context)


def downloadFile(request, file_name):
	file_path = os.path.join(MEDIA_ROOT, *file_name.split('/'))
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/pdf")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	raise Http404

@login_required(login_url="home:login")
def editArticle(request, id):
	profile = request.user.account
	try:
		old_article = profile.article_set.get(id = id)
	except:
		raise Http404

	context = {'SELECT_DAYS' : [SELECT_DAY, SELECT_MONTH, SELECT_YEAR]}
	context['accounts'] = Account.objects.all()

	if request.method == 'POST':
		formArticle = forms.ArticleForm(request.POST or None, request.FILES or None, instance=old_article)
		formTag = forms.TagForm(request.POST or None)
		formAuthor = forms.AuthorForm(request.POST or None)
		context['form_conference'] = forms.ConferenceForm()
		context['form_reviewNews'] = forms.ReviewNewsForm()
		context['form_report'] = forms.ReportForm()

		dt = str(request.POST['doctype'])
		formExtraInfo = None
		if dt == '1':
			if dt == str(old_article.doctype):
				formExtraInfo = forms.ConferenceForm(request.POST or None, instance = old_article.conference)
			else:
				formExtraInfo = forms.ConferenceForm(request.POST or None)
			context['form_conference'] = formExtraInfo
		elif dt == '2':
			if dt == str(old_article.doctype):
				formExtraInfo = forms.ReviewNewsForm(request.POST or None, instance = old_article.reviewnews)
			else:
				formExtraInfo = forms.ReviewNewsForm(request.POST or None)
			context['form_reviewNews'] = formExtraInfo
		elif dt == '3':
			if dt == str(old_article.doctype):
				formExtraInfo = forms.ReportForm(request.POST or None, instance = old_article.report)
			else:
				formExtraInfo = forms.ReportForm(request.POST or None)
			context['form_report'] = formExtraInfo

		if formArticle.is_valid() and \
			formTag.is_valid() and \
			formAuthor.is_valid() and \
			(formExtraInfo is None or formExtraInfo.is_valid()):

			old_article = profile.article_set.get(id = id)

			new_article = formArticle.save(commit = True)

			# Link extra info
			if str(new_article.doctype) != str(old_article.doctype):
				if hasattr(new_article, 'conference') :
					new_article.conference.delete()
				elif hasattr(new_article, 'reviewnews') :
					new_article.reviewnews.delete()
				elif hasattr(new_article, 'report') :
					new_article.report.delete()

				if formExtraInfo is not None:
					fei = formExtraInfo.save(commit = False)
					fei.article = new_article
					fei.save()
			elif formExtraInfo is not None:
				formExtraInfo.save(commit = True)

			# Edit authors
			for aut in old_article.author_set.all():
				if aut.user_ref is None:
					x = [0, aut.author_name]
				else:
					x = [aut.user_ref.id, aut.author_name]

				if x in formAuthor.cleaned_data['authors']:
					formAuthor.cleaned_data['authors'].remove(x)
				else:
					aut.delete()

			for aut in formAuthor.cleaned_data['authors']:
				author = models.Author(author_name = aut[1], user_ref = None, article_ref = new_article)

				if aut[0] > 0:
					try:
						user = Account.objects.get(id=aut[0])
					except Exception as e:
						pass
					else:
						author.user_ref = user

						# Create notification for identified authors
						if user != profile:
							notif = models.Notification(source = profile, destination = user, topic = new_article, notif_type = 0)
							notif.save()
							user.new_notifications = True
							user.save()
				author.save()

			# Edit tags
			for tg in old_article.tag_set.all():
				if tg.tag_name in formTag.cleaned_data['tags']:
					formTag.cleaned_data['tags'].remove(tg.tag_name)
				else:
					tg.delete()

			# Create tags
			for bubble in formTag.cleaned_data['tags']:
				tg = models.Tag(tag_name = bubble, tag_article = new_article)
				tg.save()

			# Re-Create RDF
			new_article.create_rdf(request)


			return redirect('/article/read/' + str(new_article.id))

		else:
			context['form'] = formArticle
			context['form_tag'] = formTag
			context['form_tag_errors'] = formTag['tags'].errors
			context['form_author'] = formAuthor
			context['form_author_errors'] = formAuthor['authors'].errors

			return render(request, 'accounts/edit_article.html', context)


	context['form_author'] = forms.AuthorForm()
	context['authors'] = old_article.author_set.all()
	context['form_tag'] = forms.TagForm()
	context['tags'] = old_article.tag_set.all()

	context['form_conference'] = forms.ConferenceForm()
	context['form_reviewNews'] = forms.ReviewNewsForm()
	context['form_report'] = forms.ReportForm()
	if old_article.doctype == 1:
		context['form_conference'] = forms.ConferenceForm(instance = old_article.conference)
	elif old_article.doctype == 2:
		context['form_reviewNews'] = forms.ReviewNewsForm(instance = old_article.reviewnews)
	elif old_article.doctype == 3:
		context['form_report'] = forms.ReportForm(instance = old_article.report)

	context['form'] = forms.ArticleForm(instance = old_article)
	return render(request, 'accounts/edit_article.html', context)