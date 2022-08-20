# Generated by Django 4.1 on 2022-08-18 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('learningAttendance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_number', models.CharField(max_length=30, unique=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to=users.models.path_and_rename, verbose_name='profile picture')),
                ('user_type', models.CharField(choices=[('lecturer', 'lecturer'), ('student', 'student'), ('dean', 'dean'), ('staff', 'staff')], default='student', max_length=30)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learningAttendance.course')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learningAttendance.department')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learningAttendance.school')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learningAttendance.year')),
            ],
        ),
    ]
