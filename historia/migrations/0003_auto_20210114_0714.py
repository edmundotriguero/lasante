# Generated by Django 2.2 on 2021-01-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historia', '0002_auto_20201112_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='historia',
            name='hora_proxima',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historia',
            name='fecha_proxima',
            field=models.DateField(blank=True, null=True),
        ),
    ]
