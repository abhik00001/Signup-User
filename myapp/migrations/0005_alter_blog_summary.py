# Generated by Django 5.0.4 on 2024-05-07 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_blog_content_alter_blog_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='summary',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
