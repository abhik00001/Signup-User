# Generated by Django 5.0.4 on 2024-05-06 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='Content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='summary',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
