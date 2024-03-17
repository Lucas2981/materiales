# Generated by Django 5.0.1 on 2024-03-14 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="obra2",
            name="entrega",
            field=models.DateField(
                blank=True, null=True, verbose_name="Fecha de entrega estimada"
            ),
        ),
        migrations.AlterField(
            model_name="obra2",
            name="fecha_finalizada",
            field=models.DateField(
                blank=True, null=True, verbose_name="Fecha de finalización real"
            ),
        ),
    ]