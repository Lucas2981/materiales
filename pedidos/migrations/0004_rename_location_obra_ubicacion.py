# Generated by Django 5.0.1 on 2024-01-21 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0003_rename_name_obra_obra"),
    ]

    operations = [
        migrations.RenameField(
            model_name="obra",
            old_name="location",
            new_name="ubicacion",
        ),
    ]
