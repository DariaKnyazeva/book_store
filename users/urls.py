from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import signup_customer


urlpatterns = [
    path('signup/', signup_customer, name='signup_customer'),
    # url(r'^login/$', login_view, name='login'),
    path('login/', LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'),
         name='logout'),
]
