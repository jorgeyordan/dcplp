# Generated by Django 2.0.1 on 2018-05-06 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0018_comisiones_conecta_columna_prima_operaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='comisiones_conecta',
            name='columna_prima_operaciones_oficina_plus',
            field=models.CharField(default='comision_operaciones_0', max_length=50),
        ),
    ]
