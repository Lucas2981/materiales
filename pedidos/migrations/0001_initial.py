# Generated by Django 5.0.1 on 2024-01-26 17:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="Material"
                    ),
                ),
                ("unidad", models.CharField(max_length=20, verbose_name="Unidad")),
            ],
            options={
                "verbose_name": "insumo",
                "verbose_name_plural": "insumos",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="sector",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="Sector"
                    ),
                ),
            ],
            options={
                "verbose_name": "sector",
                "verbose_name_plural": "sectores",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Obra",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Obra")),
                (
                    "location",
                    models.CharField(max_length=200, verbose_name="Ubicación"),
                ),
                (
                    "area",
                    models.CharField(
                        choices=[
                            ("0", "Escolar"),
                            ("1", "Infraestructura"),
                            ("2", "Intendencia"),
                            ("3", "Salud"),
                        ],
                        max_length=1,
                        verbose_name="Area",
                    ),
                ),
                ("contacto", models.CharField(blank=True, max_length=100)),
                (
                    "movil",
                    models.CharField(
                        blank=True, max_length=11, null=True, verbose_name="Teléfono"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Descripción",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Tec asignado",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IniciarPedidoSector",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.CharField(max_length=3, verbose_name="Cantidad")),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Creado"),
                ),
                (
                    "validated",
                    models.BooleanField(
                        default=False, editable=False, verbose_name="Aprobado"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Tec_solicitante",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pedidos.material",
                        verbose_name="Material",
                    ),
                ),
                (
                    "name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pedidos.obra",
                        verbose_name="Obra - Tec asignado",
                    ),
                ),
                (
                    "sector",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pedidos.sector",
                        verbose_name="Sector",
                    ),
                ),
            ],
            options={
                "verbose_name": "pedido",
                "verbose_name_plural": "pedidos",
                "ordering": ["-id"],
            },
        ),
    ]
