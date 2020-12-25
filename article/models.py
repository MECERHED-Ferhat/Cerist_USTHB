from django.db import models
from django.urls import reverse
from django.core.files import File
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import filesizeformat
from account.models import Account
from rdflib import Namespace, Literal, Graph, URIRef, BNode
from rdflib.namespace import RDF, XSD
import re, os

DOCTYPE_CHOICES = [
	('0', 'Other Related Productions'),
	('1', 'Conference Article'),
	('2', 'Review or Newspaper Article'),
	('3', 'Report Article')
]
NOTIFICATION_CHOICES = [
	('0', 'ACCOUNT identified you in his article ARTICLE'),
	('1', 'ACCOUNT published a new article ARTICLE')
]
AUDIENCE = [
	('0', 'National'),
	('1', 'International')
]
TYPE_RN = [
	('0', 'Article Review'),
	('1', 'Newspaper Article')
]
TYPE_RP = [
	('0', 'Research Report'),
	('1', 'Internal Report'),
	('2', 'Technical Report')
]
YES_NO = [
	('1', 'Yes'),
	('0', 'No')
]
class Tag(models.Model):

	def __str__(self):
		return str(self.tag_name)

	tag_name = models.CharField(max_length = 30)
	tag_article = models.ForeignKey('Article', on_delete=models.CASCADE)


class Author(models.Model):

	def __str__(self):
		return str(self.author_name)

	author_name = models.CharField(max_length = 180)
	user_ref = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
	article_ref = models.ForeignKey('Article', null=False, on_delete=models.CASCADE)


class Notification(models.Model):

	def __str__(self):
		return 'from '+ str(self.source.user) + ' to ' + str(self.destination.user)

	source = models.ForeignKey(Account, null=False, on_delete = models.CASCADE, related_name="src_set")
	destination = models.ForeignKey(Account, null=False, on_delete = models.CASCADE, related_name="dest_set")
	topic = models.ForeignKey("Article", null=False, on_delete = models.CASCADE)

	notif_type = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])

	seen = models.BooleanField(default = False)
	sending_date = models.DateField(auto_now_add=True)


class Article(models.Model):

	def __str__(self):
		return str(self.title)

	def _path_rdf(instance, filename):
		return "rdfs/user_{}/{}".format(instance.postmaster.id, filename)

	title = models.CharField(max_length = 60, unique=True, null=False, blank=True)
	postmaster = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
	summary = models.CharField(max_length = 2047, blank=True)
	document = models.FileField(upload_to="articles/%Y/%m/%d", null=False)
	rdf = models.FileField(upload_to=_path_rdf, null=True, blank=True)
	doctype = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
	date_creation = models.DateField(auto_now_add=True)

	def create_rdf(self, request):
		g = self.to_rdf(request)
		g.serialize("tmp_rdf.rdf", format="pretty-xml")

		with open('tmp_rdf.rdf', 'r') as f:
			filename, file_ext = os.path.splitext(os.path.basename(self.document.name))
			self.rdf.save('{0}_rdf.rdf'.format(filename), File(f))

		self.save()

	def to_rdf(self, request):
		g 				= Graph()
		si 				= Namespace(request.build_absolute_uri("/"))
		g.bind('si', si)

		q = {
			'id': self.id,
			'title': self.title,
			'postmaster': {
				'id': self.postmaster.user.id,
				'email': self.postmaster.user.email,
				'last_name': self.postmaster.user.last_name,
				'first_name': self.postmaster.user.first_name,
			},
			'summary': self.summary,
			'document': request.build_absolute_uri(self.document.url),
			'doctype': self.doctype,
			'date_creation': self.date_creation,
			'author_set': [x['author_name'] for x in list(self.author_set.values())],
			'tag_set': [x['tag_name'] for x in list(self.tag_set.values())],
		}

		extra_info = None
		if hasattr(self, 'conference'):
			extra_info = Conference.objects.filter(pk=self.conference.pk).values().first()
		elif hasattr(self, 'reviewnews'):
			extra_info = ReviewNews.objects.filter(pk=self.reviewnews.pk).values().first()
		elif hasattr(self, 'report'):
			extra_info = Report.objects.filter(pk=self.report.pk).values().first()
		if extra_info:
			for key, val in extra_info.items():
				if (key != 'article_id'):
					q[key] = val

		article 	= URIRef(request.build_absolute_uri(reverse('article:read', args=[str(q['id']),])))
		pm 				= BNode()
		tags			= BNode()
		authors		= BNode()

		nodes = []

		for key, val in q.items():
			if (key == 'postmaster'):
				nodes.append((article, si[key], pm))
				for i, j in val.items():
					nodes.append((pm, si[i], Literal(j)))
			elif (key == 'document'):
				nodes.append((article, si[key], URIRef(val)))
			elif (key == 'doctype'):
				nodes.append((article, si[key], Literal(DOCTYPE_CHOICES[int(val)][1])))
			elif (key == 'author_set'):
				nodes.append((article, si['authors'], authors))
				nodes.append((authors, RDF.type, RDF.Bag))
				for i in val:
					nodes.append((authors, RDF.li, Literal(i)))
			elif (key == 'tag_set'):
				nodes.append((article, si['tags'], tags))
				nodes.append((tags, RDF.type, RDF.Bag))
				for i in val:
					nodes.append((tags, RDF.li, Literal(i)))
			elif (key == 'audience_conference') or (key == 'audience_RN'):
				nodes.append((article, si[key], Literal(AUDIENCE[int(val)][1])))
			elif (key == 'reading_committee_conference') or (key == 'reading_committee_RN') or (key == 'procedding'):
				nodes.append((article, si[key], Literal(YES_NO[(int(val)-1)*(-1)][1])))
			elif (key == 'type_RN'):
				nodes.append((article, si[key], Literal(TYPE_RN[int(val)][1])))
			elif (key == 'type_RP'):
				nodes.append((article, si[key], Literal(TYPE_RP[int(val)][1])))
			else:
				nodes.append((article, si[key], Literal(val)))

		for i in nodes:
			g.add(i)

		return g


class Conference(models.Model):

	def __str__(self):
		return str(self.name_conference)

	article = models.OneToOneField(Article, null=True, on_delete=models.CASCADE)

	name_conference = models.CharField(max_length = 45, null=False, blank=False)
	editor_conference = models.CharField(max_length = 45, null=False, blank=False)
	audience_conference = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=False)
	reading_committee_conference = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=False)

	date_conference = models.DateField(null=False)
	location_conference = models.CharField(max_length = 45, null=False, blank=False)
	procedding = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=False)


class ReviewNews(models.Model):

	def __str__(self):
		return str(self.name_RN)

	article = models.OneToOneField(Article, null=True, on_delete=models.CASCADE)

	name_RN = models.CharField(max_length = 45, null=False, blank=False)
	editor_RN = models.CharField(max_length = 45, null=False, blank=False)
	audience_RN = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=False)
	reading_committee_RN = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=False)

	type_RN = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], null=False)
	pages = models.CharField(max_length = 20, null=True, blank=True)


class Report(models.Model):

	def __str__(self):
		return str(self.num_report)

	article = models.OneToOneField(Article, null=True, on_delete=models.CASCADE)

	type_RP = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], null=False)
	num_report = models.CharField(max_length = 45, null=False, blank=False)
