# Generated by Django 2.0.1 on 2018-04-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0008_auto_20180427_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='ot_multi_hasta20',
            name='gama_jorge',
            field=models.CharField(default='vacio', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ot_multi_hasta20',
            name='nombre_foto',
            field=models.CharField(default='cacio', max_length=100),
            preserve_default=False,
        ),
    ]