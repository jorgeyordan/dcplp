# Generated by Django 2.0.1 on 2018-04-25 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userloginactivity',
            name='dispositivo',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='dispositivofamilia',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='esbot',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='esmovil',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='espc',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='establet',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='estactil',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='familianav',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='navegador',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='os',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='osfamilia',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='osversion',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='osversion2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='versionnav',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userloginactivity',
            name='versionnav2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]