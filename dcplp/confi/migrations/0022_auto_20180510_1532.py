# Generated by Django 2.0.1 on 2018-05-10 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0021_operacionesconfiguardadas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operacionesconfiguardadas',
            old_name='mmodelo_subvecion',
            new_name='modelo_subvecion',
        ),
    ]
