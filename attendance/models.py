import datetime as dt
import math
from django.db import models
import os
from django.conf import settings

from django.urls import reverse

schools = (
    ('SAFS', 'SAFS'),
    ('SBE', 'SBE'),
    ('SCI', 'SCI'),
    ('SEA', 'SEA'),
    ('SED', 'SED'),
    ('SHS', 'SHS'),
    ('SON', 'SON'),
    ('SPAS', 'SPAS'),
    ('TVET', 'TVET'),
)
semester = (
    ('Semester1', 'Semester1'),
    ('Semester2', 'Semester2'),
    ('Semester3', 'Semester3'),

)


class Departments(models.Model):
    name = models.CharField(max_length=30)
    school = models.CharField(choices=schools, default='SBE', max_length=30)

    def __str__(self):
        return self.name[:50]


class Units(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.CharField(choices=semester, default='Semester1', max_length=30)

    def __str__(self):
        return self.name[:50]


class Student(models.Model):
    name = models.CharField(max_length=200)
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

    # def get_absolute_url(self):
    #     return reverse('course:university_detail', args=[str(self.pk)])
