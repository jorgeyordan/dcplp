# Generated by Django 2.0.1 on 2018-05-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0014_ot_multi_desde20'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comisiones_conecta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conecta', models.CharField(max_length=100)),
                ('comision', models.IntegerField()),
                ('puntos', models.IntegerField()),
                ('canales', models.IntegerField()),
            ],
        ),
    ]
