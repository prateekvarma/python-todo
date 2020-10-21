from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todoapp/home.html')

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

def loginuser(request):
    if request.method == 'GET' :
        return render(request, 'todoapp/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and paswords dont match'})
        else:
            #login the user
            login(request, user)
            #redirect to current todos page
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecomlpleted__isnull=True)
    return render(request, 'todoapp/currenttodos.html', {'todos': todos})

@login_required
def viewtodo(request, todo_pk):
    #The 'user=request.user' only pull up the todos related to specific user (owner)
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todoapp/viewtodo.html', {'todo': todo, 'form':form})
    else:
        try:
            #The 'instance=todo' below is for django to recognize it's the same todo instance to refer
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoapp/viewtodo.html', {'todo': todo, 'form':form, 'error': 'Invalid input, try again'})

@login_required
def createtodos(request):
    if request.method == 'GET':
        return render(request, 'todoapp/createtodos.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            #to save form data, but not store in DB yet, by using commit=False
            unstoredTodo = form.save(commit=False)
            #assigning user to the unstored Todo
            unstoredTodo.user = request.user
            unstoredTodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoapp/createtodos.html', {'form': TodoForm(), 'error': 'Bad data entered, try again..'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecomlpleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecomlpleted__isnull=False).order_by('-datecomlpleted')
    return render(request, 'todoapp/completedtodos.html', {'todos': todos})
