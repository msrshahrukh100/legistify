from django.shortcuts import render,HttpResponse,redirect
from booking.config import RESPONSE_FORMAT
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import copy
from .forms import *
from .models import *
from django.contrib.auth import login , logout,authenticate
from django.contrib.auth.hashers import check_password,make_password 
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings


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


def userlogin(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	form = Loginform(request.POST or None)
	if request.method == 'GET':
		context = {'form':form}
		return render(request,'signup.html',context)
	elif request.method == 'POST':
		if form.is_valid():
			print "here"
			user = Users.check_user(**dict(form.cleaned_data))
			if user:
				print "there"
				user.backend = settings.AUTHENTICATION_BACKENDS
				login(request, user)
				print request.user
				return JsonResponse({'msg':'loggedin'})
			
		else :
			return HttpResponse("shahrukh")
		# user = Users.check_user(**dict(form.cleaned_data))
		# if user:
		# 	user.backend = settings.AUTHENTICATION_BACKENDS
		# 	login(request, user)
		# 	print request.user
		# 	return JsonResponse({'msg':'loggedin'})
		# else:
		# 	return JsonResponse({'msg':'This email or password incorrect!'})



@login_required(login_url='login')
def addrequest(request):

	data = json.loads(request.body)
	user = request.user
	print user
	return JsonResponse(data)

# @login_required(login_url='login')
def userdashboard(request):
	print request.user
	response = copy.deepcopy(RESPONSE_FORMAT)
	if request.method == 'POST':
		pass
	context = {
	'lawyers' : Users.objects.all().filter(is_lawyer=True)
	}
	return render(request,'dashboard1.html',context)