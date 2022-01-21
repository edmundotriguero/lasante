# Generated by Django 2.2 on 2021-04-14 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0005_consumo_inv_multiplicador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc_ingreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('f_creacion', models.DateTimeField(auto_now_add=True)),
                ('f_modificacion', models.DateTimeField(auto_now=True)),
                ('user_updated', models.IntegerField(blank=True, null=True)),
                ('fecha', models.DateField()),
                ('razon', models.CharField(blank=True, max_length=110, null=True)),
                ('egreso_id', models.IntegerField(blank=True, null=True)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Detalle_Ingreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('f_creacion', models.DateTimeField(auto_now_add=True)),
                ('f_modificacion', models.DateTimeField(auto_now=True)),
                ('user_updated', models.IntegerField(blank=True, null=True)),
                ('cantidad_total', models.FloatField()),
                ('grupo', models.IntegerField(blank=True, null=True)),
                ('multiplicador', models.FloatField()),
                ('doc_ingreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Doc_ingreso')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Item')),
                ('unidad_medida_t', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Unidad_medida')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]