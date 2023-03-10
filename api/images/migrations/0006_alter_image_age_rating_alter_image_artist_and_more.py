# Generated by Django 4.1.5 on 2023-01-26 05:37

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_alter_category_options_alter_category_is_nsfw"),
        ("artists", "0001_initial"),
        ("characters", "0002_character_species"),
        ("images", "0005_image_dominant_color_image_primary_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="age_rating",
            field=models.CharField(
                blank=True,
                choices=[
                    ("sfw", "Sfw"),
                    ("questionable", "Questionable"),
                    ("borderline", "Borderline"),
                    ("explicit", "Explicit"),
                ],
                help_text="The image's sfw-ness.",
                max_length=12,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="artist",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="artists.artist",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="categories",
            field=models.ManyToManyField(
                blank=True, related_name="images", to="categories.category"
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="characters",
            field=models.ManyToManyField(
                blank=True, related_name="images", to="characters.character"
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="dominant_color",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.SmallIntegerField(), blank=True, null=True, size=3
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="primary_color",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.SmallIntegerField(), blank=True, null=True, size=3
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="source_name",
            field=models.CharField(
                blank=True,
                help_text="The name of the platform where the original post was posted.",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="source_url",
            field=models.URLField(
                blank=True, help_text="The image's original post.", null=True
            ),
        ),
    ]
