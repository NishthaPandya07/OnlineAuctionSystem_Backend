from django.urls import path

from . import views

app_name = 'bids'

urlpatterns = [
    path('place/<int:listing_id>/', views.place_bid, name='place'),
    path('<int:listing_id>/history/', views.bid_history, name='history'),
]
