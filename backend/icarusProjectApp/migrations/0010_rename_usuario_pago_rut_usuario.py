# Generated by Django 4.0.4 on 2022-07-03 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0009_rename_rut_usuario_pago_usuario_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pago',
            old_name='usuario',
            new_name='rut_usuario',
        ),
    ]