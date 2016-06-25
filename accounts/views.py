from django import forms
from django.contrib.auth.forms import User
from gensite.accounts.forms import MyUserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
#from django.contrib.auth.decorators import login_required

#@login_required
def my_login(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
	else:
		return HttpResponseRedirect("/test")
		
	
def register(request):
	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid() and request.POST['password1']==request.POST['password2']:
			new_user = User(username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['first_name'], email=request.POST['email'])
			new_user.set_password(request.POST['password1'])
			new_user.save()
			return HttpResponseRedirect("/home/")
	else:
		form = MyUserCreationForm()
	return render_to_response("registration/register.html", {'form' : form})

def my_home(request):
	if not request.user.is_authenticated():
		return render_to_response("index.html", {'login': False, 'index': 4})
	else:
		return render_to_response("index.html", {'login': True, 'user': request.user, 'index': 5})

