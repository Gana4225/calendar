from django.contrib import admin
from .models import *


class Res(admin.ModelAdmin):

    list_display = ["name","username", "AdmissionDate"]
    readonly_fields = ("AdmissionDate","att_status")


admin.site.register(Register, Res)