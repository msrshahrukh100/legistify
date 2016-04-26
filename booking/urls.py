from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$',home),
	url(r'^api/signup$',signup,name='signup'),
	url(r'^api/login$',userlogin,name='login'),
	url(r'^api/addrequest$',addrequest,name='addrequest'),
	url(r'^api/dashboard1$',userdashboard,name='dashboard'),

]