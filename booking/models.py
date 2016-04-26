from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import check_password,make_password 
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
# Create your models here.
class UserCustomManager(BaseUserManager):
	def create_user(self, name, email, is_lawyer=False, password=None):
		email = self.normalize_email(email)
		user = self.model(name=name,email=email,is_lawyer=is_lawyer)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,name, email, password,**extra_fields):	
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self.create_user(name,email,password)

		



class Users(AbstractBaseUser):
	name = models.CharField(max_length=50,null=False, blank=False)
	email = models.EmailField(max_length=50,null=False,unique=True	)
	is_lawyer = models.BooleanField(default=False)
	startdate = models.DateField(null=True, blank=True)
	enddate = models.DateField(null=True, blank=True)

	objects = UserCustomManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']




	@classmethod
	def checkemail(cls,email):
		try:
			data = cls.objects.get(email=email)
		except:
			data = None
		return data

	@classmethod
	def check_user(cls,**kwargs):
		pw = kwargs.get('password')
		uid = kwargs.get('email')
		user = cls.objects.get(email=uid)
		if check_password(kwargs['password'],user.password):
			return user
		else:
			return None
		


	@classmethod
	def create_user(cls,data):
		# instance = cls()
		# pw = data['password']
		# hashedpw = make_password(pw, salt=None, hasher='default')
		# instance.name = data['name']
		# instance.email = data['email']
		# instance.is_lawyer = data['is_lawyer']
		# instance.password = hashedpw
		# instance.save()
		# print instance.password
		return cls.objects.create_user(name=data['name'], email=data['email'], is_lawyer=data['is_lawyer'], password=data['password'])

	def __unicode__(self):
		return str(self.id)

class Bookingrequests(models.Model):
	description = models.TextField(max_length=100)
	from_userid = models.IntegerField(null=False, blank=False)
	to_userid = models.IntegerField(null=False, blank=False)
	date = models.DateField(null=False, blank=False)

	

	def __unicode__(self):
		return str(self.id)