from django.contrib import admin
from .models import *


#
# admin.site.register(Student)
# admin.site.register(Attendance)
# # Register your models here.

#
# class gana(admin.ModelAdmin):
#     list_display = ["name", "date"]


# admin.site.register(dim,gana)
#


class Res(admin.ModelAdmin):
    list_display = ["name","username", "AdmissionDate"]


admin.site.register(Register, Res)