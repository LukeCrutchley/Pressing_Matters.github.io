# Generated by Django 3.1.1 on 2020-09-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_auto_20200923_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
