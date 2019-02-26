from django.contrib import admin

# Register your models here.
from .models import User, Event, Restaurant
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Restaurant)

