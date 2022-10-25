# Generated by Django 4.1.1 on 2022-10-12 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_star_star'),
        ('myaccount', '0004_myaccount_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='myaccount',
            name='favorites_book',
            field=models.ManyToManyField(blank=True, related_name='favorites_books', to='book.book'),
        ),
    ]
