# Generated by Django 5.1 on 2024-08-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0002_watchlist_delete_userwatchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='overview',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='year',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='poster_path',
            field=models.CharField(default='', max_length=255),
        ),
    ]
