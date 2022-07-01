from re import search
from django.contrib import admin
from .models import Student, Units, Departments


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'year', 'semester')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'year')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')


admin.site.register(Units, UnitAdmin)

admin.site.register(Student, StudentAdmin)

admin.site.register(Departments, DepartmentAdmin)
