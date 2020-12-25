from django.shortcuts import render
from django.db.models import Q
from article import models
import re, datetime

LIST_DAY = [i for i in range(1,32)]
LIST_MONTH = [i for i in range(1,13)]
LIST_YEAR = [i for i in range(2020,2040)]

SEARCH_REGEX = r'\S+'

def _searchSort(list_title, context):
	result = []
	for seg in zip(list_title[i:] for i in range(0, len(list_title)-1)):
		for i in range(2,len(seg[0])+1):
			result.append(seg[0][0:i])
	result.sort(reverse=True, key=len)

	# Transform QuerySet into List
	old_rows = []
	for i in context['rows']:
		old_rows.append(i)

	new_rows = []
	for i in result:
		ph = ' '.join(i)
		indexs = []
		for j in range(0, len(old_rows)):
			if re.search(re.escape(ph), old_rows[j].title, re.I):
				new_rows.append(old_rows[j])
				indexs.append(j)
		for j in reversed(indexs):
			del old_rows[j]

	new_rows += old_rows

	return new_rows


def _searchTitle(list_title=None):
	out = Q(title__icontains=list_title[0])
	for i in range(1, len(list_title)):
		out = out | Q(title__icontains=list_title[i])
	return out


def _searchAuthor(list_author=None):
	out = Q(author__author_name__icontains=list_author[0])
	for i in range(1, len(list_author)):
		out = out | Q(author__author_name__icontains=list_author[i])
	return out


def _searchTag(list_tag=None):
	filters = []
	for seg in zip(list_tag[i:] for i in range(0, len(list_tag))):
		for i in range(1,len(seg[0])+1):
			filters.append(seg[0][0:i])
	filters.sort(reverse=True, key=len)
	out = Q(tag__tag_name__iexact=' '.join(filters[0]))
	for i in range(1, len(filters)):
		out = out | Q(tag__tag_name__iexact=' '.join(filters[i]))
	return out


def _searchNormal(request, context={}):
	sch = request.GET['search-bar']
	sch = re.findall(SEARCH_REGEX, sch)
	if len(sch) == 0:
		context['rows'] = models.Article.objects.all()
	else:
		context['rows'] = models.Article.objects.filter(_searchTitle(sch) | _searchAuthor(sch) | _searchTag(sch)).distinct()
		context['rows'] = _searchSort(sch, context)


def _searchFilter(request, context={}):
	title = request.GET['filter-title']
	title = re.findall(SEARCH_REGEX, title)
	if len(title) == 0:
		title = None

	author = request.GET['filter-author']
	author = re.findall(SEARCH_REGEX, author)
	if len(author) == 0:
		author = None

	doctype = request.GET['filter-doctype']
	if not (doctype in ['0', '1', '2', '3']):
		doctype = None

	if 'filter-from-none' in request.GET.keys():
		date_from = None
	else:
		try:
			date_from = datetime.date(int(request.GET['filter-from-year']),
								  	  int(request.GET['filter-from-month']),
									  int(request.GET['filter-from-day']))
		except Exception:
			date_from = None


	if 'filter-to-none' in request.GET.keys():
		date_to = None
	else:
		try:
			date_to = datetime.date(int(request.GET['filter-to-year']),
									int(request.GET['filter-to-month']),
									int(request.GET['filter-to-day']))
		except Exception:
			date_to = None

	options = {}
	options_text = []
	if title != None:
		options_text.append(_searchTitle(list_title=title) | _searchTag(list_tag=title))

	if author != None:
		options_text.append(_searchAuthor(list_author=author))

	if doctype != None:
		options['doctype__exact'] = doctype

	if date_from != None:
		options['date_creation__gte'] = date_from

	if date_to != None:
		options['date_creation__lte'] = date_to

	context['rows'] = models.Article.objects.filter(*options_text, **options).distinct()
	if title != None:
		context['rows'] = _searchSort(title, context)


# ---------- VIEWS ---------- #

def search(request, index):
	context = {}

	context['days'] = LIST_DAY
	context['months'] = LIST_MONTH
	context['years'] = LIST_YEAR

	context['rows'] = []
	context['index'] = index
	context['pages'] = []

	if request.method == 'GET' and request.GET:
		if 'search-bar' in request.GET.keys():
			_searchNormal(request, context)
		else:
			_searchFilter(request, context)
		request.session['session_rows'] = []
		request.session['session_pages'] = [i for i in range(1, (len(context['rows'])-1)//20 + 2)]
		for row in context['rows']:
			request.session['session_rows'].append(row.id)
		context['rows'] = context['rows'][:20]
	elif index in request.session['session_pages']:
		for row in request.session['session_rows'][(index-1)*20:index*20]:
			try:
				obj = models.Article.objects.get(id=row)
			except models.Article.DoesNotExist as e:
				continue
			else:
				context['rows'].append(obj)
	context['pages'] = request.session['session_pages'][(index-1)-((index-1)%3):(index-1)-((index-1)%3)+3]
	context['last_index'] = len(request.session['session_pages'])

	return render(request, 'search_article.html', context=context)


def index(request):
	context = {}
	today_date = datetime.date.today()

	class Card():
		def __init__(self, id, date, title, summary, postmaster, picture_url):
			self.id = id
			self.date = today_date - date
			self.title = title
			self.summary = summary
			self.postmaster = postmaster
			self.pic = picture_url


	context['cards'] = []

	for i in models.Article.objects.all().order_by('-date_creation')[:12]:
		pic_irl = None

		if i.postmaster.profile_pic:
			pic_irl = i.postmaster.profile_pic.url
		context['cards'].append(Card(i.id, i.date_creation, i.title, i.summary, i.postmaster.user.last_name + " " + i.postmaster.user.first_name, pic_irl))
	context['cards'].reverse()
	
	return render(request, 'index.html', context=context)