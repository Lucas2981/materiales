# Generated by Django 5.0.1 on 2024-02-08 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0011_pedido_a_proveedor"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="orden_compra",
            field=models.TextField(
                blank=True, max_length=20, null=True, verbose_name="Orden de compra"
            ),
        ),
    ]