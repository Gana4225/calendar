from django.db import models


class Register(models.Model):
    name = models.CharField(max_length=200, null=False)
    username = models.CharField(max_length=500, primary_key=True, null=False)
    password = models.CharField(max_length=100, null=False)
    phone = models.BigIntegerField(null=False)
    email = models.EmailField(null=False)
    address = models.TextField(max_length=300, null=False)
    AdmissionDate = models.DateField(null=False)
    AdmissionEnd = models.DateField(null=True)
    image = models.ImageField(upload_to="profiles", blank=True, null=False)
    att_status = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.username}"

