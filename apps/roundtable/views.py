from django.shortcuts import render, redirect, HttpResponse
from .models import User, Event, Restaurant
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

import bcrypt


def index(request):
    return render(request, 'roundtable/index.html')


def process_register(request):
    # return HttpResponse("I'm registering")
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            request.session['errors'] = errors
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            p = request.POST
            hashedpw = bcrypt.hashpw(p['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=p['first_name'], last_name=p['last_name'],
                                       email=p['email'], password=hashedpw.decode())
            request.session['user_id'] = user.id
            return redirect('/dashboard')


# LOGIN LOGOUT
def process_logout(request):
    print("logged out")
    del request.session['user_id']
    return redirect('/')


def process_login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            request.session['errors'] = errors
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            p = request.POST
            user = User.objects.filter(email=p['login_email'])[0]
            request.session['user_id'] = user.id
            return redirect('/dashboard')


def dashboard(request):
    # if 'user_id' in request.session:

    user = User.objects.get(id=request.session['user_id'])
    events = [
        {'id': 1, 'title': "nnn's birthday party", 'time': '2019-03-21', 'location': 'San Jose', 'hosted_by': "kkk",
         'guests': ['aaa', 'bbb', 'ccc']},
        {'id': 2, 'title': "kkk's birthday party", 'time': '2019-03-21', 'location': 'San Jose', 'hosted_by': "nnn",
         'guests': ['aaa', 'bbb', 'ccc']},
        {'id': 3, 'title': "www's birthday party", 'time': '2019-03-21', 'location': 'San Jose', 'hosted_by': "kkk",
         'guests': ['aaa', 'bbb', 'ccc']},
        {'id': 4, 'title': "fff's birthday party", 'time': '2019-03-21', 'location': 'San Jose', 'hosted_by': "kkk",
         'guests': ['aaa', 'bbb', 'ccc']},
    ]
    context = {
        'user': user,
        'events': events
    }

    return render(request, 'roundtable/dashboard.html', context)


# else:
#     return redirect("/")


def createevent(request):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        'user': user
    }

    return render(request, 'roundtable/createevent.html', context)
