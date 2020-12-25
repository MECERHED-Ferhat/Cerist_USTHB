from django.urls import path
from home import views 
from account import views as accountViews



app_name = 'home'

urlpatterns = [
	path('', views.index, name='index'),
	path('search/<int:index>/', views.search, name='search'),
	path('register/',accountViews.registration,name="register"),
	path('registration-done/',accountViews.registrationDone,name="registrationDone"),
	path('activate-account/<uidb64>/<token>/',accountViews.activateAccount,name="activate"),
	path('login/',accountViews.loginPage,name='login'),
	path('logout/',accountViews.logoutPage,name='logout'),
	
]
