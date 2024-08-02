
from django.urls import path
from django.contrib import admin
from . import views  # Import your views module

urlpatterns = [
    path('home/', views.home, name='home'),
    path('index/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('viewTechnicians/',views.viewTechnicians,name='viewTechnicians'),
    path('viewAirplanes/',views.viewAirplanes,name='viewAirplanes'),
    path('viewTestingevents/',views.viewTestingevents,name='viewTestingevents'),
    path('addTestevent/',views.addTestevent,name='addTestevent'),
    path('addTechnicians/',views.addTechnicians,name='addTechnicians'),
    path('addPlanes/',views.addPlanes,name='addPlanes'),
    path('removeTechnician/',views.removeTechnician,name='removeTechnician'),
]