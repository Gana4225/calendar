from django.urls import path
from .views import *


urlpatterns = [
      path('', attendance_calendar, name='attendance_calendar'),
      path("login/", clogin, name="clogin")
]