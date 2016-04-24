from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import check_password,make_password 
# Create your models here.

class Users(models.Model):
	name = models.CharField(max_length=50,null=False, blank=False)
	email = models.EmailField(max_length=50,null=False, blank=False,default='')
	is_lawyer = models.BooleanField(default=False)
	startdate = models.DateField(null=True, blank=True)
	enddate = models.DateField(null=True, blank=True)
	password = models.CharField(max_length=30,null=False, blank=False)
	def clean(self):
		if self.startdate < self.enddate:
			raise ValidationError("End date must be after start date")

	@classmethod
	def checkemail(cls,email):
		try:
			data = cls.objects.get(email=email)
		except:
			data = None
		return data

	@classmethod
	def create_user(cls,data):
		instance = cls()
		pw = data['password']
		hashedpw = make_password(pw, salt=None, hasher='default')
		instance.name = data['name']
		instance.password = hashedpw
		instance.save()
		print instance.password

	def __unicode__(self):
		return str(self.id)

class Bookingrequests(models.Model):
	description = models.TextField(max_length=100)
	from_userid = models.IntegerField(null=False, blank=False)
	to_userid = models.IntegerField(null=False, blank=False)
	date = models.DateField(null=False, blank=False)

	def __unicode__(self):
		return str(self.id)