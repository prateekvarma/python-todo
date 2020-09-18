from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

def signupuser(request):
    if request.method == 'GET' :
        return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm()})
    else:
        #check password
        if request.POST['password1'] == request.POST['password2']:
            try:               
                #create a new user
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                #login the user after signup
                login(request, user)
                #redirect to current todos page
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm(), 'error':'Username alredy exists'})
        else:
            #passwords dont match
            return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords dont match'})
            
def currenttodos(request):
    return render(request, 'todoapp/currenttodos.html')