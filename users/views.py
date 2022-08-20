from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from users.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import User, UserProfile


def studentPanel(request):
    student_info = UserProfile.objects.all()
    context = {
        'user': student_info,

    }
    return render(request, 'student_panel.html', context)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm
        profile_form = UserProfileInfoForm
    context = {
        'registered': registered,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration.html', context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('users:student_panel'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please use correct id and password")
    else:
        return render(request, 'login.html')
           


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('meru_learning:schools_list'))


@login_required
def profile(request):
    profile_info = User.objects.all()
    context = {
        ' user': profile_info,

    }
    return render(request, 'profile.html', context)
