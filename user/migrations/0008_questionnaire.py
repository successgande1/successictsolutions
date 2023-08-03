# Generated by Django 4.0.6 on 2023-04-11 21:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0007_remove_profile_phone_alter_education_qualification_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computerkn', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=100, null=True)),
                ('ownlaptop', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=100, null=True)),
                ('ownphone', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=100, null=True)),
                ('browseint', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=100, null=True)),
                ('knowwebdev', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=100, null=True)),
                ('littleprogram', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=100, null=True)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('applicant', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]