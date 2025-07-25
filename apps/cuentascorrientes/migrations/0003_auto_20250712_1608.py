# Generated by Django 3.1 on 2025-07-12 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cuentascorrientes', '0002_listaprecios_remitos_remitosdet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='domicilio_departamento',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='domicilio_piso',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='localidad',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuentascorrientes.provincias'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='telefono_celular',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='telefono_fijo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuentascorrientes.tiposcliente'),
        ),
    ]
