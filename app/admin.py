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

class Ros(admin.ModelAdmin):
    list_display = ["name", "att_status"]


admin.site.register(AttStatus,Ros)