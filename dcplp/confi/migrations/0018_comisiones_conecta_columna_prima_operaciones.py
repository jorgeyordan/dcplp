# Generated by Django 2.0.1 on 2018-05-06 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0017_comisiones_conecta_valor_volumen'),
    ]

    operations = [
        migrations.AddField(
            model_name='comisiones_conecta',
            name='columna_prima_operaciones',
            field=models.CharField(default='acelerador_conecta_4', max_length=50),
        ),
    ]