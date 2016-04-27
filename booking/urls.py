from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$',signup,name='signup'),
	url(r'^api/login$',userlogin,name='login'),
	url(r'^api/dashboard1$',userdashboard,name='userdashboard'),
	url(r'^api/dashboard2$',lawyerdashboard,name='lawyerdashboard'),
	url(r'^api/acceptrequest/(?P<id>\d+)/$',acceptrequest,name='acceptrequest'),
	url(r'^api/denyrequest/(?P<id>\d+)/$',denyrequest,name='denyrequest'),
	url(r'^api/logout$',logout_view,name='logout'),


]