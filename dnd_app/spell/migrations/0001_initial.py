# Generated by Django 5.1.7 on 2025-04-12 13:46

import django.db.models.deletion
import functools
import utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("character_class", "0001_initial"),
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CastingTime",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "approximate_time_in_seconds",
                    models.IntegerField(
                        default=3,
                        validators=[utils.validators.validate_positive_integer],
                    ),
                ),
            ],
            options={
                "ordering": ("approximate_time_in_seconds",),
            },
        ),
        migrations.CreateModel(
            name="MagicAuraStrength",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MagicSchool",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpellComponent",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("short_name", models.CharField(max_length=2, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpellDescriptor",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpellRange",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MagicSubSchool",
            fields=[
                (
                    "magicschool_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="spell.magicschool",
                    ),
                ),
            ],
            bases=("spell.magicschool",),
        ),
        migrations.CreateModel(
            name="Spell",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=4000, null=True),
                ),
                ("link", models.URLField(blank=True, null=True)),
                ("target", models.CharField(blank=True, max_length=50, null=True)),
                ("effect", models.CharField(blank=True, max_length=50, null=True)),
                ("area", models.CharField(blank=True, max_length=50, null=True)),
                ("duration", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "saving_throw",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "spell_resistance",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "casting_time",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="spell.castingtime",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="spell.magicschool",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="common.source",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpellLevel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "level",
                    models.IntegerField(
                        default=1,
                        validators=[
                            functools.partial(
                                utils.validators.validate_integer_in_range,
                                *(),
                                **{"max_value": 9, "min_value": 0},
                            )
                        ],
                    ),
                ),
                (
                    "character_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="character_class.characterclass",
                    ),
                ),
                (
                    "spell",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spell.spell"
                    ),
                ),
            ],
            options={
                "unique_together": {("spell", "character_class")},
            },
        ),
        migrations.AddField(
            model_name="spell",
            name="level",
            field=models.ManyToManyField(
                blank=True,
                through="spell.SpellLevel",
                to="character_class.characterclass",
            ),
        ),
        migrations.AddField(
            model_name="spell",
            name="range",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="spell.spellrange"
            ),
        ),
        migrations.CreateModel(
            name="SpellSpellComponent",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="spell.spellcomponent",
                    ),
                ),
                (
                    "spell",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spell.spell"
                    ),
                ),
            ],
            options={
                "verbose_name": "Spell Component",
                "verbose_name_plural": "Spell Components",
                "unique_together": {("spell", "component")},
            },
        ),
        migrations.AddField(
            model_name="spell",
            name="components",
            field=models.ManyToManyField(
                blank=True,
                through="spell.SpellSpellComponent",
                to="spell.spellcomponent",
            ),
        ),
        migrations.CreateModel(
            name="SpellSpellDescriptor",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "descriptor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="spell.spelldescriptor",
                    ),
                ),
                (
                    "spell",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spell.spell"
                    ),
                ),
            ],
            options={
                "verbose_name": "Spell Descriptor",
                "verbose_name_plural": "Spell Descriptors",
                "unique_together": {("spell", "descriptor")},
            },
        ),
        migrations.AddField(
            model_name="spell",
            name="descriptor",
            field=models.ManyToManyField(
                blank=True,
                through="spell.SpellSpellDescriptor",
                to="spell.spelldescriptor",
            ),
        ),
        migrations.AddField(
            model_name="spell",
            name="subschool",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="spell_subschool",
                to="spell.magicsubschool",
            ),
        ),
    ]
