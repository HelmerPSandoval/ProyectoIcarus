# Generated by Django 4.0.4 on 2022-07-03 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0010_rename_usuario_pago_rut_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]