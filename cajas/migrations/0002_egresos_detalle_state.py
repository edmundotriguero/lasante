# Generated by Django 2.2 on 2021-04-14 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='egresos',
            name='detalle_state',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
