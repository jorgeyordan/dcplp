# Generated by Django 2.0.1 on 2018-04-26 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0002_auto_20180425_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='userloginactivity',
            name='city',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='country',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='lat',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='longi',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
