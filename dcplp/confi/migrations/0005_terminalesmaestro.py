# Generated by Django 2.0.1 on 2018-04-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confi', '0004_userloginactivity_login_logout'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerminalesMaestro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=500)),
                ('nombre_foto', models.CharField(max_length=500)),
                ('tipo_jorge', models.CharField(max_length=500)),
            ],
        ),
    ]
