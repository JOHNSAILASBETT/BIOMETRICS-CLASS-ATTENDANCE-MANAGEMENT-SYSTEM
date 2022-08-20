from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    mail = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        labels = {
            'password1': 'password',
            'password2': 'Confirm password',
        }


class UserProfileInfoForm(forms.ModelForm):
    reg_number = forms.CharField(required=True)
    lecturer = 'lecturer'
    student = 'student'
    dean = 'dean'
    staff = 'staff'
    
    user_types = [
        (student, 'student'),
    ]
    user_type = forms.ChoiceField(required=True, choices=user_types)

    class Meta:
        model = UserProfile
        fields = ('reg_number', 'profile_pic', 'user_type', 'school', 'department', 'course', 'year')
  