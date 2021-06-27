# Generated by Django 3.1.4 on 2021-01-05 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='bid',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.bids'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='items',
            name='min_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Minimum price'),
        ),
    ]