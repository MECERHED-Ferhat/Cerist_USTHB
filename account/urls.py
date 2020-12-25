from django.urls import path
from account import views



app_name = 'account'

urlpatterns = [
	path('basic-information/',views.accountBasicInformation,name='basicInformation'),
    path('change-password/',views.changePassword,name='changePassword'),
    path('delete-account/',views.deleteAccount,name='deleteAccount'),
    path('<int:id>+<str:last_name>+<str:first_name>/',views.account,name='profile'),
    path('notifications/', views.notifications, name='notifications')
]

