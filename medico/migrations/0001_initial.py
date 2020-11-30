# Generated by Django 2.2 on 2020-11-10 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paciente', '0002_auto_20201104_2015'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('f_creacion', models.DateTimeField(auto_now_add=True)),
                ('f_modificacion', models.DateTimeField(auto_now=True)),
                ('user_updated', models.IntegerField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('f_creacion', models.DateTimeField(auto_now_add=True)),
                ('f_modificacion', models.DateTimeField(auto_now=True)),
                ('user_updated', models.IntegerField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=50)),
                ('detalles', models.TextField(blank=True, null=True)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('f_creacion', models.DateTimeField(auto_now_add=True)),
                ('f_modificacion', models.DateTimeField(auto_now=True)),
                ('user_updated', models.IntegerField(blank=True, null=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('documento_identificacion', models.CharField(max_length=50, unique=True)),
                ('fecha_nacimiento', models.DateField()),
                ('celular', models.CharField(max_length=30)),
                ('correo', models.CharField(max_length=255, unique=True)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.Ciudad')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.Especialidad')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.Genero')),
                ('tipo_documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.Tipo_documento')),
                ('turno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.Turno')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]