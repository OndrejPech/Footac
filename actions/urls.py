"""actions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from .views import home_view, club_view, team_actions_view

app_name = 'actions'
urlpatterns = [
    path('', home_view, name='home'),
    path('clubs/<int:club_id>/', club_view, name='club_detail'),
    path('teams/<int:team_id>/actions', team_actions_view, name='team_actions'),
]

# conventions
# list /cars/
# create /cars/new/
# detail /cars/1/
# update /cars/1/edit/
# delete /cars/1/delete/
# any methods not dependent on an object /cars/view-name/
# any methods dependent on a particular object /cars/1/view-name/
