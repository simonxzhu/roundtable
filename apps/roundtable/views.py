from yelpapi import YelpAPI

from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

from datetime import datetime
import pprint
import re
import bcrypt

from .models import User, Event, Restaurant, Rating, Ratings


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


icon_map = {
    (Ratings.Love, "fa-heart"),
    (Ratings.Like, "fa-thumps-up"),
    (Ratings.Okay, "fa-check-square"),
    (Ratings.Dislike, "fa-thumbs-down"),
    (Ratings.Hate, "fa-ban"),
}

def dashboard(request):
    # if 'user_id' in request.session:

    user = User.objects.get(id=request.session['user_id'])

    events = Event.objects.all().order_by('time')
    context = {
        'user': user,
        'users': User.objects.all(),
        'events': events,
        'icon_map': icon_map,
    }

    return render(request, 'roundtable/dashboard.html', context)


def createevent(request):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        'user': user
    }

    return render(request, 'roundtable/createevent.html', context)


def process_addevent(request):
    form = request.POST

    event = Event.objects.create(
        title=form['title'],
        time=form['time'],
        location=form['location'],
        hosted_by=User.objects.get(id=request.session['user_id']),
        )

    # XXX Add validations!
    # XX This is hardcoded to 3 restaurants, use jquery to do something smarter
    url_pattern = r'https://www.yelp.com/biz/(.+)'
    url = ""
    n = 1
    rest = 'rest' + str(n)
    rest_obj = None
    while rest in form:

        if form[rest]:
            try:
                rest_url = form[rest].split("?")[0]
                url = re.search(url_pattern, rest_url).group(1)
            except AttributeError:
                print("url not found.. should have been caught by validator")
                url=""
        print(url)

        if url != "":
            try:
                rest_obj = Restaurant.objects.get(alias=url)
            except Restaurant.DoesNotExist:
                print(f'Querying API for rest1 = {url}')
                yelp_api = YelpAPI('MC6wAGZjDLn5g6voWircN7C5T2nUmO39cxHDteSV-RTOsrDi7od0jgX_yEmjVfeVvfoss9VvNJfXHSiAO10PeKrl0fsStcap41hghJynCziWLYF_u21VgSP4g5d1XHYx')

                r = yelp_api.business_query(id=url)
                pprint.pprint(r)
                photo1_url = ""
                photo2_url = ""
                photo3_url = ""
                if len(r['photos']) > 0:
                    photo1_url = r['photos'][0]
                if len(r['photos']) > 1:
                    photo2_url = r['photos'][1]
                if len(r['photos']) > 2:
                    photo3_url = r['photos'][2]
                rest_obj = Restaurant.objects.create(
                    alias=r['alias'],
                    name=r['name'],
                    image_url=r['image_url'],
                    url=r['url'],
                    display_phone=r['display_phone'],
                    review_count=r['review_count'],
                    rating=r['rating'],
                    photo1_url=photo1_url,
                    photo2_url=photo2_url,
                    photo3_url=photo3_url,
                    # price=r['price']
                )
            event.restaurants.add(rest_obj)
            event.save()
        n += 1
        rest = 'rest' + str(n)

    return redirect("/dashboard")

def process_delete(request, id):
    Event.objects.get(id=id).delete()
    return redirect("/dashboard")


def process_search(request):
    if 'search_url' in request.session or 'top_restaurants' in request.session:
        del request.session['search_url']
        del request.session['top_restaurants']

    form = request.POST
    # googlemaps display
    googlemaps_url = f"https://www.google.com/maps/embed/v1/search?key=AIzaSyAaduuGxiWech24CbaFGc1OoHEt10Kr9fI&q=restaurant+in+{form['location']}"
    request.session['search_url'] = googlemaps_url

    # yelpapi call
    yelp_api = YelpAPI(
        'MC6wAGZjDLn5g6voWircN7C5T2nUmO39cxHDteSV-RTOsrDi7od0jgX_yEmjVfeVvfoss9VvNJfXHSiAO10PeKrl0fsStcap41hghJynCziWLYF_u21VgSP4g5d1XHYx')
    businesses = yelp_api.search_query(term='restaurant', location=form['location'], sort_by='rating', limit=5)['businesses']
    # shape the response (name, image_url, url)
    restaurant = {}
    result = []
    for business in businesses:
        for k, v in business.items():
            if k == "name" or k == "image_url" or k == "url":
                restaurant[k] = v
        result.append(restaurant)
        restaurant = {}
    request.session['top_restaurants'] = result

    return redirect("/events/new")


def link_restaurant(request, event_id):
    form = request.POST
    url_pattern = r'https://www.yelp.com/biz/(.+)'
    url1 = ""
    event = Event.objects.get(id=event_id)
    if form['rest']:
        try:
            rest = form['rest'].split("?")[0]
            url1 = re.search(url_pattern, rest).group(1)
        except AttributeError:
            print("url not found.. should have been caught by validator")
    print(url1)
    new_rest = None
    if rest != "":
        try:
            new_rest = Restaurant.objects.get(alias=url1)
        except Restaurant.DoesNotExist:
            print(f'Querying API for rest1 = {url1}')
            yelp_api = YelpAPI(
                'MC6wAGZjDLn5g6voWircN7C5T2nUmO39cxHDteSV-RTOsrDi7od0jgX_yEmjVfeVvfoss9VvNJfXHSiAO10PeKrl0fsStcap41hghJynCziWLYF_u21VgSP4g5d1XHYx')

            r = yelp_api.business_query(id=url1)
            pprint.pprint(r)
            photo1_url = ""
            photo2_url = ""
            photo3_url = ""
            if len(r['photos']) > 0:
                photo1_url = r['photos'][0]
            if len(r['photos']) > 1:
                photo2_url = r['photos'][1]
            if len(r['photos']) > 2:
                photo3_url = r['photos'][2]
            new_rest = Restaurant.objects.create(
                alias=r['alias'],
                name=r['name'],
                image_url=r['image_url'],
                url=r['url'],
                display_phone=r['display_phone'],
                review_count=r['review_count'],
                rating=r['rating'],
                photo1_url=photo1_url,
                photo2_url=photo2_url,
                photo3_url=photo3_url,
                # price=r['price']
            )
        event.restaurants.add(new_rest)
        event.save()

    return redirect('/dashboard')


def link_guest(request, event_id):
    user = User.objects.get(id=request.POST['guest_id'])
    event = Event.objects.get(id=event_id)
    event.users_who_join.add(user)

    return redirect('/dashboard')
