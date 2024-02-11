# Generated by Django 5.0.1 on 2024-02-10 21:03

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
            name="Material",
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
                (
                    "referencia",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Referencia"
                    ),
                ),
            ],
            options={
                "verbose_name": "insumo",
                "verbose_name_plural": "insumos",
                "ordering": ["rubro", "name"],
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
                (
                    "name",
                    models.CharField(max_length=200, unique=True, verbose_name="Obra"),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Ubicación"
                    ),
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
                (
                    "dpto",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Departamento",
                    ),
                ),
                (
                    "localidad",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Localidad"
                    ),
                ),
                (
                    "municipio",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Municipio"
                    ),
                ),
                (
                    "frac",
                    models.CharField(
                        blank=True, max_length=2, null=True, verbose_name="Fracción"
                    ),
                ),
                (
                    "radio",
                    models.CharField(
                        blank=True, max_length=2, null=True, verbose_name="Radio"
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Tipo"
                    ),
                ),
                (
                    "internacion",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Internación",
                    ),
                ),
                (
                    "nivel_sector",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Nivel/Sector",
                    ),
                ),
                (
                    "plaza",
                    models.IntegerField(blank=True, null=True, verbose_name="Plaza"),
                ),
                (
                    "lugar",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Lugar"
                    ),
                ),
                ("cue", models.IntegerField(blank=True, null=True, verbose_name="CUE")),
                (
                    "anexo",
                    models.CharField(
                        blank=True, max_length=2, null=True, verbose_name="Anexo"
                    ),
                ),
                ("cp", models.IntegerField(blank=True, null=True, verbose_name="C.P.")),
                (
                    "periodo_func",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Periodo de Funcionamiento",
                    ),
                ),
                (
                    "geometry",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Georeferencia",
                    ),
                ),
            ],
            options={
                "verbose_name": "obra",
                "verbose_name_plural": "obras",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Rubros",
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
                    models.CharField(max_length=150, unique=True, verbose_name="Rubro"),
                ),
                (
                    "referencia",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Referencia"
                    ),
                ),
            ],
            options={
                "verbose_name": "rubro",
                "verbose_name_plural": "rubros",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Sector",
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
            name="MaterialesPedido",
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
                ("cantidad", models.IntegerField()),
                (
                    "material",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pedidos.material",
                    ),
                ),
            ],
            options={
                "verbose_name": "material",
                "verbose_name_plural": "materiales",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Pedido",
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
                    "memoria",
                    models.TextField(
                        blank=True,
                        help_text="En este campo, debes explicar brevemente el problema que quieres resolver y la solución que propones con los materiales que solicitas. Usa un lenguaje claro, conciso y preciso para expresar tu idea.",
                        max_length=500,
                        null=True,
                        verbose_name="Memoria",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Fecha de solicitud"
                    ),
                ),
                (
                    "validated",
                    models.BooleanField(default=False, verbose_name="Autorizado"),
                ),
                (
                    "a_proveedor",
                    models.BooleanField(default=False, verbose_name="A Proveedor"),
                ),
                (
                    "orden_compra",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        unique=True,
                        verbose_name="Orden de compra",
                    ),
                ),
                (
                    "materiales",
                    models.ManyToManyField(
                        blank=True,
                        through="pedidos.MaterialesPedido",
                        to="pedidos.material",
                    ),
                ),
                (
                    "obra",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pedidos.obra"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Tec asignado",
                    ),
                ),
            ],
            options={
                "verbose_name": "pedido",
                "verbose_name_plural": "pedidos",
                "ordering": ["-id"],
            },
        ),
        migrations.AddField(
            model_name="materialespedido",
            name="pedido",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="pedidos.pedido",
            ),
        ),
        migrations.AddField(
            model_name="material",
            name="rubro",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="pedidos.rubros",
                verbose_name="Rubro",
            ),
        ),
        migrations.AddField(
            model_name="materialespedido",
            name="sector",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pedidos.sector"
            ),
        ),
    ]
