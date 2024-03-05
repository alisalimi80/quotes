from django.urls import path 
from . import views

app_name = 'auote_app'

urlpatterns = [ 
    path('quotes/',views.QuoteAllView.as_view(),name='quotes'),
    path('quotes/<str:pk>',views.QuoteDetailView.as_view(),name='quotes_detail'),
    path('quote_delete/<int:pk>/',views.QuoteDeleteView.as_view(),name='quote_delete'),
    path('quote_create/',views.QuoteCreateView.as_view(),name='quote_create'),
    path('quote_update/<int:pk>/',views.QuoteUpdateView.as_view(),name='quote_update'),
    path('tag_create/',views.CreatTagView.as_view(),name='tag_create'),
    path('tags/',views.TagAllView.as_view(),name='tags'),
]