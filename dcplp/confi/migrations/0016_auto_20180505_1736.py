# Generated by Django 2.0.1 on 2018-05-05 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0015_comisiones_conecta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ot_multi_desde20',
            options={'ordering': ['modelo']},
        ),
        migrations.AddField(
            model_name='terminalesmaestro',
            name='foto_modelo',
            field=models.ImageField(default='verde', upload_to='static/images/terminales_modelos/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='terminalesmaestro',
            name='info_modelo',
            field=models.TextField(default='verde'),
            preserve_default=False,
        ),
    ]
