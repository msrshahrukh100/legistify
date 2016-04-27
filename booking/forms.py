from .models import *
from django import forms

class Signupform(forms.ModelForm):
	password = forms.CharField(min_length=5)
	class Meta:
		model = Users
		fields = ["name","email","is_lawyer"]


class Loginform(forms.Form):
	email = forms.EmailField()
	password = forms.CharField()

class Lawyerform(forms.ModelForm):
	class Meta:
		model = Users
		fields = ['startdate','enddate']





