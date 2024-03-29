# Generated by Django 5.0.1 on 2024-03-16 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0007_alter_pedido_memoria_alter_pedido_problema_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="memoria",
            field=models.CharField(
                blank=True, max_length=2000, null=True, verbose_name="Memoria"
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="problema",
            field=models.TextField(
                blank=True,
                help_text="En este campo, debes explicar brevemente el problema que quieres resolver.",
                max_length=6000,
                null=True,
                verbose_name="Planteo de problema",
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="propuesta",
            field=models.TextField(
                blank=True,
                help_text="En este campo, debes explicar brevemente la solución que quieres implementar.",
                max_length=6000,
                null=True,
                verbose_name="Propuesta de solución",
            ),
        ),
    ]
