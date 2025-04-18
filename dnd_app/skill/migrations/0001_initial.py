# Generated by Django 5.1.7 on 2025-04-12 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("trained_only", models.BooleanField(default=False)),
                ("armor_check_penalty", models.BooleanField(default=False)),
                (
                    "description",
                    models.TextField(blank=True, max_length=3000, null=True),
                ),
                ("link", models.URLField(blank=True, null=True)),
                (
                    "ability",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="common.ability"
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
    ]
