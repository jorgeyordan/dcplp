# Generated by Django 2.0.1 on 2018-04-22 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserLoginActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_IP', models.GenericIPAddressField(blank=True, null=True)),
                ('login_datetime', models.DateTimeField(auto_now=True)),
                ('login_username', models.CharField(blank=True, max_length=40, null=True)),
                ('user_agent_info', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'user_login_activity',
                'verbose_name_plural': 'user_login_activities',
            },
        ),
    ]
