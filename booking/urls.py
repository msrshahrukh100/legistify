from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$',home),
	url(r'^api/signup$',signup,name='signup'),
	url(r'^api/login$',userlogin,name='login'),
	url(r'^api/dashboard1$',userdashboard,name='userdashboard'),
	url(r'^api/dashboard2$',lawyerdashboard,name='lawyerdashboard'),
	url(r'^api/acceptrequest/(?P<id>\d+)/$',acceptrequest,name='acceptrequest'),


]