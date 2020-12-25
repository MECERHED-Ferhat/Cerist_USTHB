from faker import Faker
import random, sys, os, django, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from article import models as art_model
from account import models as acc_model
from django.contrib.auth.models import User

fake = Faker()

cpt = 5
if len(sys.argv) == 2:
	cpt = int(sys.argv[1])

for x in range(cpt):
	list_account = acc_model.Account.objects.all()
	extra_arg = {}
	extra_arg['last_name'] = fake.last_name()
	extra_arg['first_name'] = fake.first_name()
	extra_arg['username'] = extra_arg['last_name'] + '_' + extra_arg['first_name']
	extra_arg['password'] = 'testage'
	extra_arg['email'] = fake.ascii_free_email()

	acc_model.AllowedEmail.objects.create(email=extra_arg['email'])
	instance_acc = User.objects.create(**extra_arg)
	instance_acc = acc_model.Account.objects.create(user=instance_acc)

	for acc in list_account:
		acc.follow.add(instance_acc)
		instance_acc.follow.add(acc)
		acc.save()
		instance_acc.save()

list_account = acc_model.Account.objects.all()

for x in range(cpt*4):
	extra_arg = {}
	extra_arg['title'] = fake.sentence(nb_words = 10)
	extra_arg['postmaster'] = random.choice(list_account)
	extra_arg['summary'] = ' '.join(fake.paragraphs(nb = 20))
	extra_arg['document'] = "articles/2020/08/29/cursive-handwriting-worksheets.pdf"
	extra_arg['doctype'] = random.randint(0,3)

	art = art_model.Article.objects.create(**extra_arg)

	extra_arg = {'article' : art}
	if art.doctype == 1 or art.doctype == 2:
		name_crn = fake.sentence(nb_words=5)
		editor_crn = fake.company()
		audience_crn = random.randint(0,1)
		reading_committee = random.randint(0,1)

		if art.doctype == 1:
			extra_arg['name_conference'] = name_crn
			extra_arg['editor_conference'] = editor_crn
			extra_arg['audience_conference'] = audience_crn
			extra_arg['reading_committee_conference'] = reading_committee
			extra_arg['date_conference'] = fake.date_object()
			extra_arg['location_conference'] = fake.address()
			extra_arg['procedding'] = random.randint(0,1)

			art_model.Conference.objects.create(**extra_arg)
		else:
			extra_arg['name_RN'] = name_crn
			extra_arg['editor_RN'] = editor_crn
			extra_arg['audience_RN'] = audience_crn
			extra_arg['reading_committee_RN'] = reading_committee
			extra_arg['type_RN'] = random.randint(0,1)
			rint = random.randint(0,9999)
			extra_arg['pages'] = 'pp ' + str(rint) + '-' + str(random.randint(rint,9999))

			art_model.ReviewNews.objects.create(**extra_arg)

	elif art.doctype == 3:
		extra_arg['type_RP'] = random.randint(0,2)
		extra_arg['num_report'] = fake.ean()

		art_model.Report.objects.create(**extra_arg)


	for i in range(random.randint(1,7)):
		extra_arg = {}
		author_random = random.choice(list_account)
		author_choice = random.choice((
							(author_random.user.last_name+' '+author_random.user.first_name, author_random),
							(fake.name(), None)
						))
		extra_arg['author_name'] = author_choice[0]
		extra_arg['user_ref'] = author_choice[1]
		extra_arg['article_ref'] = art

		notif_arg = {}
		if author_choice[1] is not None:
			notif_arg['source'] = art.postmaster
			notif_arg['destination'] = author_choice[1]
			notif_arg['topic'] = art
			notif_arg['notif_type'] = 0

			art_model.Notification.objects.create(**notif_arg)

		art_model.Author.objects.create(**extra_arg)

	for i in range(random.randint(0,10)):
		extra_arg = {}
		extra_arg['tag_name'] = fake.word()
		extra_arg['tag_article'] = art

		art_model.Tag.objects.create(**extra_arg)
