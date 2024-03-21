# Generated by Django 4.2.6 on 2024-01-24 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='description',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='cover_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='publication_date',
            new_name='publidate',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='stock_quantity',
            new_name='quantity',
        ),
    ]