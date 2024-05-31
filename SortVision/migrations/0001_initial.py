# Generated by Django 5.0.6 on 2024-05-31 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Kraj",
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
                ("nazwa", models.CharField(max_length=100)),
                ("w_finale", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Main",
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
                ("Opis", models.TextField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Final",
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
                ("nazwa", models.CharField(default="Finał", max_length=100)),
                (
                    "kraje",
                    models.ManyToManyField(related_name="finaly", to="SortVision.kraj"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Polfinal",
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
                ("numer", models.PositiveIntegerField()),
                (
                    "kraje",
                    models.ManyToManyField(
                        related_name="polfinaly", to="SortVision.kraj"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PunktacjaJury",
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
                ("punkty", models.PositiveIntegerField()),
                (
                    "final",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="punkty_jury",
                        to="SortVision.final",
                    ),
                ),
                (
                    "kraj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="otrzymane_punkty_jury",
                        to="SortVision.kraj",
                    ),
                ),
                (
                    "polfinal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="punkty_jury",
                        to="SortVision.polfinal",
                    ),
                ),
                (
                    "przyznajacy_kraj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="przyznane_punkty_jury",
                        to="SortVision.kraj",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PunktacjaWidzowie",
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
                ("punkty", models.PositiveIntegerField()),
                (
                    "final",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="punkty_widzowie",
                        to="SortVision.final",
                    ),
                ),
                (
                    "kraj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="otrzymane_punkty_widzowie",
                        to="SortVision.kraj",
                    ),
                ),
                (
                    "polfinal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="punkty_widzowie",
                        to="SortVision.polfinal",
                    ),
                ),
            ],
        ),
    ]
