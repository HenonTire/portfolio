from django.urls import path
from .views import contact, list_schedules

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('list_schedules/', list_schedules, name='list_schedules'),
]
