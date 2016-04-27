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
from datetime import datetime
import re
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.

def convert_to_date_object(date):
    """Converting date string to datetime.date object."""
    try:
        re.sub("[\-\/\:]+", "-", date)
        return datetime.strptime(date, "%Y-%m-%d").date()
    except:
        return None



def signup(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	form = Signupform(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			data = form.cleaned_data
			Users.create_user(data=data)
			response['message'] = "Successfully registered!"
			messages.success(request, 'Successfully registered. Login to continue.')
			return redirect('signup')
	context = {'form':form}
	return render(request,'signup.html',context)


def userlogin(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	form = Loginform(request.POST or None)
	if request.method == 'GET':
		context = {'form':form}
		return render(request,'login.html',context)
	elif request.method == 'POST':
		if form.is_valid():
			user = Users.check_user(**dict(form.cleaned_data))
			if user:
				user.backend = settings.AUTHENTICATION_BACKENDS
				login(request, user)
				if user.is_lawyer :
					return redirect('lawyerdashboard')
				else:
					return redirect('userdashboard')
			else:
				messages.error(request,"Invalid login credentials")
				return redirect('login')
		else :
			messages.error(request,"Invalid login credentials")
			return redirect('login')


@login_required(login_url='login')
def lawyerdashboard(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	user = request.user
	form = Lawyerform(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			sd = form.cleaned_data['startdate']
			ed = form.cleaned_data['enddate']
			if ed < sd :
				messages.error(request,"Start date should be less than end date")
				return redirect('lawyerdashboard')
			else:
				user.startdate = form.cleaned_data['startdate']
				user.enddate = form.cleaned_data['enddate']
				user.save()
	context = {
	'bookingrequests' : Bookingrequests.objects.all().filter(to_userid=user.id),
	'form' : form,
	'user' : user,
	}
	return render(request,'dashboard2.html',context)



@login_required(login_url='login')
def userdashboard(request):
	response = copy.deepcopy(RESPONSE_FORMAT)
	user = request.user
	if request.method == 'POST':
		data = json.loads(request.body)
		if not data.get('lawyer',None):
			return JsonResponse({'msg':'Select a lawyer'})
		lawyer = Users.objects.get(id=data['lawyer'])
		data['date'] = convert_to_date_object(str(data['date']))
		if 	lawyer.startdate and lawyer.enddate:
			if  data['date'] < lawyer.startdate or data['date'] > lawyer.enddate:
				return JsonResponse({'msg':'The selected lawyer is not available for this date!'})
		instance = Bookingrequests.addrequest(**dict(data=data,user=user.id,email=user.email))
		return JsonResponse({'msg':'Request is sent to the selected lawyer'})
	context = {
	'bookingrequests' : Bookingrequests.objects.all().filter(from_userid=user.id),
	'lawyers' : Users.objects.all().filter(is_lawyer=True),
	'user' : user,
	}
	return render(request,'dashboard1.html',context)



@login_required()
def acceptrequest(request,id=None):
	instance = Bookingrequests.objects.get(id=id)
	mail = instance.from_email
	message = "Your request for a lawyer on Legistify.com has been accepted.Please contact the lawyer."
	instance.accepted = True
	instance.save()
	send_mail('Lawyer Request Confirmation Email', message, 'msr.concordfly@gmail.com',[mail], fail_silently=False)
	return JsonResponse({"msg":"Mail has been sent to the client"})
	
@login_required()
def denyrequest(request,id=None):
	instance = Bookingrequests.objects.get(id=id)
	instance.denied = True
	instance.save()
	return JsonResponse({"msg":"The request is denied"})
	


	

def logout_view(request):
    logout(request)
    return redirect('signup')
    # Redirect to a success page.
