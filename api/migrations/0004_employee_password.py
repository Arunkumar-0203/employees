# Generated by Django 5.0.6 on 2024-11-04 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_employee_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
