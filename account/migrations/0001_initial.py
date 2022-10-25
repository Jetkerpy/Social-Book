# Generated by Django 4.1.1 on 2022-09-25 22:05

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_img', models.ImageField(default='no.jpg', upload_to=account.models.profile_img)),
                ('hide_email', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
