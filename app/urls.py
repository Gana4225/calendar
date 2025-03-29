from django.urls import path
from .views import *
from .utils import verify, forgetpass


urlpatterns = [
      path('', attendance_calendar, name='attendance_calendar'),
      path("login/", clogin, name="login"),
      path("register/", cregister, name="register"),
      path("logout/", clogout, name="logout"),
      path("verify/<str:token>/", verify, name="verify"),
      path("forget/<str:token>/", forgetpass, name="forget"),
]