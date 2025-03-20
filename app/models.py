from django.db import models

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
#
#     def __str__(self):
#         return f"{self.student.name} - {self.date} - {self.status}"
#
#
# class dim(models.Model):
#     name = models.CharField(max_length=200)
#     date = models.DateField(auto_now=True)
#
#
#     def __str__(self):
#         return self.name
#

class AttStatus(models.Model):
    name = models.CharField(max_length=200)
    att_status = models.JSONField(default=list)