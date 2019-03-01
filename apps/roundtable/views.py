from yelpapi import YelpAPI
from python_project.settings import yelp_key, googlemap_key
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q, Avg
from django.contrib import messages
from django.utils import timezone

from datetime import datetime
import pprint
import re
import bcrypt

from .models import User, Event, Restaurant, Rating


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
            if 'invite_event' in request.session:
                event_id = request.session['invite_event']
                del request.session['invite_event']
                event = Event.objects.get(id=event_id)
                event.users_who_join.add(User.objects.get(id=request.session['user_id']))
                event.save()
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
            if 'invite_event' in request.session:
                event_id = request.session['invite_event']
                del request.session['invite_event']
                event = Event.objects.get(id=event_id)
                event.users_who_join.add(User.objects.get(id=request.session['user_id']))
                event.save()
            return redirect('/dashboard')




def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        events = Event.objects.all().order_by('time')
        context = {
            'user': user,
            'users': User.objects.all(),
            'events': events,
        }

    user = User.objects.get(id=request.session['user_id'])

    events = Event.objects.filter(users_who_join__id__contains=user.id).order_by('time')

    context = {
        'user': user,
        'users': User.objects.all(),
        'events': events,
    }
    return render(request, 'roundtable/dashboard.html', context)



def createevent(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }

    return render(request, 'roundtable/createevent.html', context)


def process_addevent(request):
    m = request.POST['message']
    # print("&"*50, m)
    errors = Event.objects.basic_validator(request.POST)
    if len(errors) > 0:
        request.session['errors'] = errors
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/events/new')

    # if no errors
    form = request.POST
    event = Event.objects.create(
        title=form['title'],
        time=form['time'],
        location=form['location'],
        message=form['message'],
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
        # print(url)

        if url != "":
            try:
                rest_obj = Restaurant.objects.get(alias=url)
            except Restaurant.DoesNotExist:
                print(f'Querying API for rest1 = {url}')
                yelp_api = YelpAPI(yelp_key)

                r = yelp_api.business_query(id=url)
                # pprint.pprint(r)
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
        n += 1
        rest = 'rest' + str(n)

    event.users_who_join.add(User.objects.get(id=request.session['user_id']))
    event.save()
    return redirect("/dashboard")


def process_delete(request, id):
    Event.objects.get(id=id).delete()
    return redirect("/dashboard")


def process_search(request):
    form = request.GET
    # print(form)
    # googlemaps display
    googlemaps_url = f"https://www.google.com/maps/embed/v1/search?key={googlemap_key}&q={form['food_type']}+in+{form['location']}"
    request.session['search_url'] = googlemaps_url
    # print(googlemaps_url)
    # yelpapi call
    yelp_api = YelpAPI(yelp_key)
    businesses = yelp_api.search_query(term=form['food_type'], location=form['location'], sort_by='rating', limit=5)['businesses']
    # shape the response (name, image_url, url)
    # pprint.pprint(businesses)
    restaurant = {}
    result = []
    for business in businesses:
        for k, v in business.items():
            if k == "name" or k == "image_url" or k == "url":
                restaurant[k] = v
        result.append(restaurant)
        restaurant = {}
    request.session['top_restaurants'] = result
    context = {
        'googlemaps_url': googlemaps_url,
        'top_restaurants': result
    }

    return render(request, 'roundtable/partials/rests_map.html', context)



def process_vote(request):
    form = request.GET
    value = form['value']
    cell = value.split(',')
    rate = Rating.objects.filter(restaurant__id=cell[1], rater__id=cell[2])
    if len(rate) < 1:
        rate = Rating.objects.create(restaurant=Restaurant.objects.get(id=cell[1]), rater=User.objects.get(id=cell[2]), rating=cell[3])
    else:
        print(f"saving new rating {cell[3]}")
        my_rate = rate.first()
        my_rate.rating = cell[3]
        my_rate.save()
    all_ratings = Rating.objects.filter(restaurant__id=cell[1])
    avg_query = all_ratings.all().aggregate(Avg('rating'))
    average = avg_query['rating__avg']
    average_icon = 'far fa-check-square'
    if average > 1:
        average_icon = 'far fa-heart'
    elif average > 0:
        average_icon = 'far fa-thumbs-up'
    elif average > -1:
        average_icon = 'far fa-check-square'
    elif average > -2:
        average_icon = 'far fa-thumbs-down'
    else:
        average_icon = 'fas fa-ban'
    
    context = {
        'average': average_icon
    }
    return render(request, 'roundtable/partials/score.html', context)


def link_restaurant(request, event_id):
    form = request.POST
    url_pattern = r'https://www.yelp.com/biz/(.+)'
    url1 = ""
    event = Event.objects.get(id=event_id)
    rest = ""
    if form['rest']:
        try:
            rest = form['rest'].split("?")[0]
            url1 = re.search(url_pattern, rest).group(1)
        except AttributeError:
            rest = ""
            print("url not found.. should have been caught by validator")
    # print(url1)
    new_rest = None
    if rest != "":
        try:
            new_rest = Restaurant.objects.get(alias=url1)
        except Restaurant.DoesNotExist:
            print(f'Querying API for rest1 = {url1}')
            yelp_api = YelpAPI(yelp_key)

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
    print("$" * 50, request.POST['guest_name'])
    if len(request.POST['guest_name'].strip()) == 0:
        return redirect('/dashboard')

    full_name = request.POST['guest_name'].split(' ')
    event = Event.objects.get(id=event_id)
    if len(full_name) < 2:
        user = User.objects.filter(first_name__iexact=full_name[0]).first()
    else:
        user = User.objects.filter(first_name__iexact=full_name[0], last_name__iexact=full_name[1]).first()

    if user == None:
        print("User doesn't exist")
        return redirect('/dashboard')
    if user in event.users_who_join.all():
        print("User has been invited")
        return redirect('/dashboard')
    else:
        print("Add user successfully")
        event.users_who_join.add(user)
        return redirect('/dashboard')


def editevent(request, event_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'event': event,
        'user': user,
        'time': event.time.isoformat("|", timespec='hours')
    }

    return render(request, 'roundtable/editevent.html', context)


def handle_invite(request, event_id):
    event = Event.objects.get(id=event_id)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        events = Event.objects.filter(users_who_join__id__contains=user.id)
        if len(events) == 0:
            already_joined = False
        else:
            already_joined = True
    else:
        user = None;
        already_joined = False

    context = {
        'event': event,
        'user': user,
        'already_joined': already_joined
    }

    return render(request, 'roundtable/invite.html', context)

def handle_accept(request, event_id):
    if 'user_id' in request.session:
        event = Event.objects.get(id=event_id)
        event.users_who_join.add(User.objects.get(id=request.session['user_id']))
        event.save()
        return redirect("/dashboard")
    else:
        request.session['invite_event'] = event_id
        return redirect("/")



def process_update(request, event_id):
    errors = Event.objects.basic_validator(request.POST)
    if len(errors) > 0:
        request.session['errors'] = errors
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f'/events/edit/{event_id}')

    # if no errors
    form = request.POST
    event = Event.objects.get(id=event_id)
    event.title = form['title']
    event.time = form['time']
    event.location = form['location']
    event.hosted_by = event.hosted_by
    event.message = form['message']
    event.save()


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
                url = ""
        print(url)

        if url != "":
            try:
                rest_obj = Restaurant.objects.get(alias=url)
            except Restaurant.DoesNotExist:
                print(f'Querying API for rest1 = {url}')
                yelp_api = YelpAPI(yelp_key)

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
        n += 1
        rest = 'rest' + str(n)

    # event.users_who_join.add(User.objects.get(id=request.session['user_id']))
    event.save()

    return redirect("/dashboard")
