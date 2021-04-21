from pricing.api import views

from django.urls import path

app_name = 'pricing-api'


urlpatterns = [
    path('currency/', views.ListCreateCurrencyView.as_view(), name='currency'),
    path('currency/<int:pk>/', views.RetrieveCurrencyView.as_view(), name='currency'),

    path('category/', views.ListCreatePriceView.as_view(), name='category'),
    path('category/<int:pk>/', views.RetrievePriceView.as_view(), name='category'),
]
