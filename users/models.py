from django.db import models
from django.contrib.auth.models import User
import os
from learningAttendance.models import Year, School, Department, Course


def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]

    if instance.user.username:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.user.username, ext)
    return os.path.join(upload_to, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=30, unique=True)
    profile_pic = models.ImageField(upload_to=path_and_rename, verbose_name='profile picture', blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    lecturer = 'lecturer'
    student = 'student'
    dean = 'dean'
    staff = 'staff'

    user_types = [
        (lecturer, 'lecturer'),
        (student, 'student'),
        (dean, 'dean'),
        (staff, 'staff'),

    ]
    user_type = models.CharField(max_length=30, choices=user_types, default=student)
