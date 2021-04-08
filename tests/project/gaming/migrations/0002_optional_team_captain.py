# Generated by Django 3.1.7 on 2021-04-08 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gaming", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="captain",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="led_teams",
                to="gaming.player",
            ),
        ),
    ]