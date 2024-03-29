# Generated by Django 4.0.6 on 2023-03-25 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_course_date_course_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='mstatus',
            new_name='marital_status',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.CharField(blank=True, choices=[('Computer Litracy Application Form', 'Computer Litracy Application Form'), ('Computer Applications Training Form', 'Computer Applications Training Form'), ('Front-End Web Development Form', 'Front-End Web Development Form'), ('BCKEND. TRN. FORM', 'BCKEND. TRN. FORM'), ('COMPT. LIT. TRN. FEE', 'COMPT. LIT. TRN. FEE'), ('APP. TRN. FEE', 'APP. TRN. FEE'), ('FRNTEND. TRN. FEE', 'FRNTEND. TRN. FEE'), ('BCKEND. TRN. FEE', 'BCKEND. TRN. FEE'), ('PROJ. BASED. AGREE. FORM', 'PROJ. BASED. AGREE. FORM')], default=None, max_length=100, null=True),
        ),
    ]
