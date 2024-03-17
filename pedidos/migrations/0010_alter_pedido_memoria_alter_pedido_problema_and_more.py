# Generated by Django 5.0.1 on 2024-03-17 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0009_alter_pedido_memoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="memoria",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Memoria enriquecida sobre el problema",
                max_length=3000,
                null=True,
                verbose_name="Memoria",
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="problema",
            field=models.TextField(
                blank=True,
                help_text="Explicar brevemente el problema que quieres resolver.",
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
                help_text="Explicar brevemente la solución que quieres implementar.",
                max_length=6000,
                null=True,
                verbose_name="Propuesta de solución",
            ),
        ),
    ]
