# Generated by Django 5.0.4 on 2024-05-10 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
