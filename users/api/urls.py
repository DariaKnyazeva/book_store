from users.api import views

from django.urls import path

app_name = 'users-api'


urlpatterns = [
    path('user/<int:pk>/', views.RetrieveUserView.as_view(), name='user'),
]
