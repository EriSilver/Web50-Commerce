# Generated by Django 3.1.4 on 2021-01-05 14:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlists'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlists',
            name='wdate',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
