# Generated by Django 4.0.4 on 2022-06-27 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0004_alter_vuelo_fecha_llegada_alter_vuelo_fecha_salida'),
    ]

    operations = [
        migrations.AddField(
            model_name='vuelo',
            name='hora_llegada',
            field=models.TimeField(default='00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vuelo',
            name='hora_salida',
            field=models.TimeField(default='00:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vuelo',
            name='id_ciudad_destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_ciudad_destino', to='icarusProjectApp.ciudad'),
        ),
        migrations.AlterField(
            model_name='vuelo',
            name='id_ciudad_origen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_ciudad_origen', to='icarusProjectApp.ciudad'),
        ),
    ]
