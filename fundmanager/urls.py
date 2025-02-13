from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.signin, name='signin'),
    path('register/', views.register),
    path('event-details/<int:id>', views.event_details, name='event_details'),
    path('create-event/', views.create_event, name='create_event'),
    path('create-event/<int:id>', views.create_event, name='create_event'),
]