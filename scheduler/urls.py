from django.urls import path
from scheduler.views import TestView, RegisterTimeView, TimeSlotView



urlpatterns = [
    path('home/', TestView.as_view(), name='TestView'),
    path('timeslots/', TimeSlotView.as_view(), name='TimeSlotView'),
    path('register/', RegisterTimeView.as_view(), name='RegisterTimeView'),
]

