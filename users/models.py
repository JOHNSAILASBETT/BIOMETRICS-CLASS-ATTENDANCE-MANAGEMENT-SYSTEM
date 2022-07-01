from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime as dt
import math
from attendance.models import schools, Departments


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length= 30)
    last_name = models.CharField(max_length=30)
    reg_no = models.CharField(primary_key=True, unique=True, max_length=30)
    image = models.ImageField(upload_to="static/images/students", null=True, blank=True)
    school = models.CharField(choices=schools, default='science_&_computing', max_length=30)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    year = models.IntegerField(max_length=10)
    date_of_admission = models.DateField()

    def year(self):
        days = (dt.date.today() - self.date_of_admission).days
        years = math.floor(days / 365)
        return years

    def __str__(self):
        return self.name[:50]
