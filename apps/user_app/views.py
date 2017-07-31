from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.db.models import Count

def index(request):
    return render(request, 'user_app/index.html')

def register(request):
    user = User.userManager.register(request.POST["first_name"],request.POST["last_name"],request.POST["email"],request.POST["password"],request.POST["conf_password"], request.POST['birthday'])
    if user[0]:
        request.session['loggedUser'] = user[1].first_name
        request.session['loggedUserID'] = user[1].id
        return redirect('/quotes')
    else:
        for error in user[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def login(request):
    user = User.userManager.login(request.POST["email"], request.POST["password"])
    if user[0]:
        request.session['loggedUser'] = user[1].first_name
        request.session['loggedUserID'] = user[1].id
        return redirect('/quotes')
    else:
        for error in user[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect ('/')
