# Generated by Django 4.0.4 on 2022-07-10 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0014_alter_usuario_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]