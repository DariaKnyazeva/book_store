from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import signup_customer

# app_name = 'users'

urlpatterns = [
    path('signup/', signup_customer, name='signup_customer'),
    path('login/', LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'),
         name='logout'),
]
