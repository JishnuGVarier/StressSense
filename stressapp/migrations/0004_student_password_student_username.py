# Generated by Django 5.0.3 on 2024-04-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stressapp', '0003_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
