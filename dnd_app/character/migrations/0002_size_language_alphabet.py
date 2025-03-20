# Generated by Django 5.1.7 on 2025-03-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("character", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Size",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=15, unique=True)),
                ("size_modifier", models.IntegerField(default=0)),
                ("grapple_modifier", models.IntegerField(default=0)),
                ("height_or_length", models.CharField(max_length=25)),
                ("weight", models.CharField(max_length=25)),
                ("space_ft", models.DecimalField(decimal_places=1, max_digits=2)),
                ("natural_reach_tall_ft", models.IntegerField(default=0)),
                ("natural_reach_long_ft", models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name="language",
            name="alphabet",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
