# Generated by Django 5.2.3 on 2025-06-26 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vuelos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fila', models.PositiveIntegerField()),
                ('columna', models.CharField(max_length=1)),
                ('tipo', models.CharField(choices=[('ventana', 'Ventana'), ('pasillo', 'Pasillo'), ('medio', 'Medio')], max_length=10)),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('reservado', 'Reservado'), ('ocupado', 'Ocupado')], default='disponible', max_length=10)),
                ('avion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asientos', to='vuelos.avion')),
            ],
            options={
                'verbose_name': 'Asiento',
                'verbose_name_plural': 'Asientos',
                'ordering': ['avion', 'fila', 'columna'],
                'unique_together': {('avion', 'fila', 'columna')},
            },
        ),
    ]
