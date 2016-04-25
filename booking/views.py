from django.shortcuts import render,HttpResponse
from booking.config import RESPONSE_FORMAT
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import copy
from .forms import *
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password,make_password 
import json


# Create your views here.

def home(request):
	return HttpResponse("shahrukh")


def signup(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	form = Signupform(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			if len(form.cleaned_data.get('password')) < 5 or Users.checkemail(form.cleaned_data.get('email')):
				if len(form.cleaned_data.get('password')) < 5:
					response['errors'] = "Password length too short.Should be more than 5."
				if Users.checkemail(form.cleaned_data.get('email')):
					response['errors'] = "Email is already taken!"
			else:
				data = form.cleaned_data
				Users.create_user(data=data)
				response['message'] = "Successfully registered!"
			return JsonResponse(response)
	context = {'form':form}
	return render(request,'signup.html',context)


def login(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	form = Loginform(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			if len(form.cleaned_data.get('password')) < 5:
				response['errors'] = "Password length too short.Should be more than 5."
			else:
				if Users.checkemail(form.cleaned_data.get('email')):
					data = form.cleaned_data
					user = Users.checkemail(form.cleaned_data.get('email'))
					if check_password(data['password'],user.password):
						login(request,user)
					else:
						response['errors'] = "Entered password is incorrect!"

				else:
					response['errors'] = "This email id is not registered with us!"
			return JsonResponse(response)
	context = {'form':form}
	return render(request,'signup.html',context)



def addrequest(request):
	data = json.loads(request.body)
	# context={'msg':data.get('description')}
	return JsonResponse(data,safe=False)

def userdashboard(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	if request.method == 'POST':
		pass
	context = {
	'lawyers' : Users.objects.all().filter(is_lawyer=True)
	}
	return render(request,'dashboard1.html',context)