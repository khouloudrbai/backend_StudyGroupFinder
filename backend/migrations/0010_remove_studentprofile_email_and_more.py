# Generated by Django 5.1.2 on 2024-11-19 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_studentprofile_github_studentprofile_linkedin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='username',
        ),
    ]
