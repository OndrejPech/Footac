from django.urls import path, include
from .views import login_user, logout_user, register_user, show_profile, \
    edit_profile, change_password


app_name = 'accounts'
urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register_user, name='register'),
    path('profile/', show_profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
]
