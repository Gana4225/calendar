from django.urls import path
from .views import attendance_calendar


urlpatterns = [
      path('', attendance_calendar, name='attendance_calendar'),
]