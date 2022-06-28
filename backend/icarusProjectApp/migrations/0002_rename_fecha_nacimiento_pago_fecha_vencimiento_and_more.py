from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icarusProjectApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pago',
            old_name='fecha_vencimiento',
            new_name='fecha_vencimiento',
        ),
        migrations.AlterField(
            model_name='avion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ciudad',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='pago',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rut',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='vuelo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]