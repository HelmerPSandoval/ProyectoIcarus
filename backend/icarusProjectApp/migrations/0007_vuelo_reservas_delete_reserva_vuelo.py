# Generated by Django 4.0.4 on 2022-07-02 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0006_alter_usuario_email_alter_usuario_nombre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vuelo',
            name='reservas',
            field=models.ManyToManyField(blank=True, to='icarusProjectApp.reserva'),
        ),
        migrations.DeleteModel(
            name='Reserva_Vuelo',
        ),
    ]