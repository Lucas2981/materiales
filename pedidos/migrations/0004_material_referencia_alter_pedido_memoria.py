# Generated by Django 5.0.1 on 2024-02-03 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0003_alter_pedido_memoria_alter_pedido_validated"),
    ]

    operations = [
        migrations.AddField(
            model_name="material",
            name="referencia",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Referencia"
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="memoria",
            field=models.TextField(
                blank=True,
                help_text="En este campo, debes explicar brevemente el problema que quieres resolver y la solución que propones con los materiales que solicitas. Usa un lenguaje claro, conciso y preciso para expresar tu idea.",
                max_length=500,
                null=True,
                verbose_name="Memoria",
            ),
        ),
    ]