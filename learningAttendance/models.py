from django.db import models
from django.http import HttpResponse
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import User
from django.urls import reverse


def save_school_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.name:
        filename = 'School_Pictures/{}.{}'.format(instance.name, ext)
    return os.path.join(upload_to, filename)


class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_school_image, blank=True, verbose_name='school image')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Year(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


SEMESTER = (
    ('Semester_1', 'Semester_1'),
    ('Semester_2', 'Semester_2'),
    ('Semester_3', 'Semester_3'),
)


# class Semester(models.Model):
#     name = models.CharField(
#         max_length=30,
#         choices=SEMESTER,
#         default='semester_1',
#         null=True,
#     )
#
#     slug = models.SlugField(null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super().save(*args, **kwargs)
#

def save_department_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.name:
        filename = 'Department_Pictures/{}.{}'.format(instance.name, ext)
    return os.path.join(upload_to, filename)


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    image = models.ImageField(upload_to=save_department_image, blank=True, verbose_name='department image')
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def save_course_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.course_name:
        filename = 'Course_Pictures/{}.{}'.format(instance.course_name, ext)
    return os.path.join(upload_to, filename)


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to=save_course_image, blank=True, verbose_name='course image')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.course_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_name)
        super().save(*args, **kwargs)


def save_unit_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.unit_name:
        filename = 'Unit_Pictures/{}.{}'.format(instance.unit_name, ext)
    return os.path.join(upload_to, filename)


class Unit(models.Model):
    unit_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    semester = models.CharField(
        max_length=30,
        choices=SEMESTER,
        default='semester_1',
        null=True,
    )
    image = models.ImageField(upload_to=save_unit_image, blank=True, verbose_name='unit image')
    is_offered = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.unit_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.unit_name)
        super().save(*args, **kwargs)


def save_lecture_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lecture_name:
        filename = 'lecture_files/{}/{}.{}'.format(instance.lecture_name, instance.lecture_name, ext)
        if os.path.exists(filename):
            new_name = str(instance.lecture_name) + str('1')
            filename = 'Lecture_images/{}/{}.{}'.format(instance.lecture_name, new_name, ext)
    return os.path.join(upload_to, filename)


class Lecture(models.Model):
    lecture_name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lectures')
    position = models.PositiveSmallIntegerField(verbose_name='Chapter no.')
    slug = models.SlugField(null=True, blank=True)
    # position represents chaters...1 is chapter one and so on
    video = models.FileField(upload_to=save_lecture_files, verbose_name='video', blank=True)
    ppt = models.FileField(upload_to=save_lecture_files, verbose_name='presentation', blank=True, null=True)
    notes = models.FileField(upload_to=save_lecture_files, verbose_name='notes', blank=True, null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.lecture_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.lecture_name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('curriculum:lesson_list', kwargs={'slug': self.subject.slug, 'standard': self.standard.slug})

# class Comment(models.Model):
#     unit_name = models.ForeignKey(Lecture, null=True, on_delete=models.CASCADE, related_name='comments')
#     comm_name = models.CharField(max_length=100, blank=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.TextField(max_length=500)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.comm_name

#     class Meta:
#         ordering = ['date_added']


# class Reply(models.Model):
#     comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
#     reply_body = models.TextField(max_length=500)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return 'reply to' + str(self.comment_name.comm_name)
