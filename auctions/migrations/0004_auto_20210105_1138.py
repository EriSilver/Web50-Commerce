# Generated by Django 3.1.4 on 2021-01-05 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210105_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='bid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.bids'),
        ),
    ]
