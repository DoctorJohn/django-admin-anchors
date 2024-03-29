# Generated by Django 3.1.7 on 2021-04-01 20:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                (
                    "captain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="led_teams",
                        to="gaming.player",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(related_name="teams", to="gaming.Player"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to="gaming.player",
                    ),
                ),
            ],
        ),
    ]
