from pricing.api import views

from django.urls import path

app_name = 'pricing-api'


urlpatterns = [
    path('currencies/', views.ListCreateCurrencyView.as_view(), name='currency'),
    path('currencies/<int:pk>/', views.RetrieveCurrencyView.as_view(), name='currency'),

    path('categories/', views.ListCreatePriceView.as_view(), name='category'),
    path('categories/<int:pk>/', views.RetrievePriceView.as_view(), name='category'),
]
