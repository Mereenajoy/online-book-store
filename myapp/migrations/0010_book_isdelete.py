# Generated by Django 4.2.6 on 2024-03-04 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_book_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isdelete',
            field=models.BooleanField(default=False),
        ),
    ]