# Generated by Django 5.0.1 on 2024-03-16 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0004_pedido_propuesta_alter_pedido_memoria"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pedido",
            old_name="memoria",
            new_name="problema",
        ),
    ]
