from pricing.api import views

from django.urls import path

app_name = 'pricing-api'


urlpatterns = [
    path('currency/', views.ListCreateCurrencyView.as_view(), name='currency'),
    path('currency/<int:pk>/', views.RetrieveCurrencyView.as_view(), name='currency'),

    path('price/', views.ListCreatePriceView.as_view(), name='price'),
    path('price/<int:pk>/', views.RetrievePriceView.as_view(), name='price'),
]
