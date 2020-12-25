from django.urls import path
from article import views


app_name = 'article'

urlpatterns = [
	path('add/', views.addArticle, name='addArticle'),
	path('read/<int:id>/', views.readArticle, name='read'),
	path('download/<path:file_name>', views.downloadFile, name='download'),
	path('edit/<int:id>/', views.editArticle, name='editArticle')
]