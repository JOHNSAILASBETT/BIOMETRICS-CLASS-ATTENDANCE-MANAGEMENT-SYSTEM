from django.views.generic import ListView, DetailView

# from .models import Course, University, Entry
from django.contrib.auth import authenticate, login
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy


def index(request):
    return render(request, "index.html")


def students(request):
    student = Entry.objects.all()
    context = {
        'student': student,

    }
    return render(request, "students.html", context)
