# Generated by Django 4.0.6 on 2023-04-12 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_rename_can_browse_internet_questionnaire_browse_internet_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='browse_internet',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='know_programming',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='own_laptop',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='own_phone',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='web_development',
        ),
    ]
