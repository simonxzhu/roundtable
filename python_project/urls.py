"""python_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.roundtable.urls')),

<<<<<<< HEAD
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#
# urlpatterns = [
#     url(r'^', include('apps.application.urls')),
#     url(r'^login/', include('apps.login.urls')),
#     url(r'^wall/', include('apps.wall.urls')),
#     url(r'^shows/', include('apps.shows.urls')),
#     url(r'^favoritebooks/', include('apps.favoritebooks.urls')),
#     url(r'^admin/', admin.site.urls),
# ]
=======
]
>>>>>>> 47e25e05090bf77a7edcc02daa0654b91a283687
