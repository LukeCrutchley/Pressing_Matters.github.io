# Generated by Django 3.1.1 on 2020-09-22 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_auto_20200922_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlist',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('ckosed', 'Closed')], default='Open', max_length=100),
        ),
    ]