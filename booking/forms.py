from .models import *
from django import forms

class Signupform(forms.ModelForm):
	class Meta:
		model = Users
		fields = ["name","email","is_lawyer","password"]


class Loginform(forms.Form):
	email = forms.EmailField()
	password = forms.CharField()





