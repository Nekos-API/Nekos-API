# Generated by Django 4.1.5 on 2023-01-26 04:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "description",
                    models.CharField(
                        help_text="A short description that describes when this category applies.",
                        max_length=256,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("character", "Character"),
                            ("setting", "Setting"),
                            ("format", "Format"),
                        ],
                        max_length=9,
                        null=True,
                    ),
                ),
                (
                    "is_nsfw",
                    models.BooleanField(
                        default=False,
                        help_text="Wether the name or description of the category contain NSFW content or not.",
                        verbose_name="Is the name or description NSFW?",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
