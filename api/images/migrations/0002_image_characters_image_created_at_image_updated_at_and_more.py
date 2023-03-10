# Generated by Django 4.1.5 on 2023-01-26 02:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("characters", "0001_initial"),
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="characters",
            field=models.ManyToManyField(
                related_name="images", to="characters.character"
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="image",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="image",
            name="age_rating",
            field=models.CharField(
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
            name="aspect_ratio",
            field=models.CharField(
                help_text="The image's aspect ratio (w:h).", max_length=11
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="height",
            field=models.SmallIntegerField(
                default=0, help_text="The image's height in pixels."
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="is_original",
            field=models.BooleanField(
                default=False,
                help_text="Wether the image was illustrated by the original artist of the characters that appear in it.",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="source_name",
            field=models.CharField(
                help_text="The name of the platform where the original post was posted.",
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="source_url",
            field=models.URLField(help_text="The image's original post.", null=True),
        ),
        migrations.AlterField(
            model_name="image",
            name="width",
            field=models.SmallIntegerField(
                default=0, help_text="The image's width in pixels."
            ),
        ),
    ]
