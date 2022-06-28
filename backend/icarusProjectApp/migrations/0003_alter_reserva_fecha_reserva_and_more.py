from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0002_rename_fecha_nacimiento_pago_fecha_vencimiento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha_reserva',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='vuelo',
            name='fecha_llegada',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='vuelo',
            name='fecha_salida',
            field=models.DateTimeField(),
        ),
    ]