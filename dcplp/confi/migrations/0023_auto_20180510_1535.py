# Generated by Django 2.0.1 on 2018-05-10 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0022_auto_20180510_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operacionesconfiguardadas',
            old_name='modelo_subvecion',
            new_name='modelo_subvencion',
        ),
    ]