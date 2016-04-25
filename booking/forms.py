from .models import *
from django import forms

class Signupform(forms.ModelForm):
	class Meta:
		model = Users
		fields = ["name","email","is_lawyer","password"]


class Loginform(forms.ModelForm):
	class Meta:
		model = Users
		fields = ["email","password"]





