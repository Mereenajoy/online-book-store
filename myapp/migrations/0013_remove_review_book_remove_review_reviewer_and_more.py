# Generated by Django 4.2.6 on 2024-03-18 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_book_isdelete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='book',
        ),
        migrations.RemoveField(
            model_name='review',
            name='reviewer',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]