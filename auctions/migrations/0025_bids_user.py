# Generated by Django 3.1.1 on 2020-09-19 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_auto_20200919_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
