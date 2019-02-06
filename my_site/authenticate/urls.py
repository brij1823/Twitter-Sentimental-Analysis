from django.urls import path
from . import views
from .views import get_data
from django.conf.urls import url
urlpatterns = [
	path('', views.home,name="home"),
	path('login/', views.login_user,name='login'),
	path('logout/',views.logout_user,name='logout'),
	path('register/',views.register,name='register'),
	path('datapassing/',views.datapassing,name='datapass'),

    
    #path('getdata/',views.get_data,name='getdata'),
	
]
