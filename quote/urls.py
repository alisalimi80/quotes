from django.urls import path 
from . import views

app_name = 'auote_app'

urlpatterns = [ 
    path('quotes/',views.QuoteAllView.as_view(),name='quotes'),
    path('quote_delete/',views.QuoteDeleteView.as_view(),name='quote_delete'),
    path('quote_create/',views.QuoteCreateView.as_view(),name='quote_create'),
    path('quote_update/',views.QuoteUpdateView.as_view(),name='quote_update'),
]