# Generated by Django 4.0.4 on 2022-07-10 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0013_alter_ciudad_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]