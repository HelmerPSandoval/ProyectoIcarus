# Generated by Django 4.0.4 on 2022-06-24 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0004_usuario_last_login_usuario_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.IntegerField(null=True),
        ),
    ]