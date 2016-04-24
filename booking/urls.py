from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$',home),
	url(r'^api/signup$',signup),
	url(r'^api/dashboard1$',userdashboard),

]