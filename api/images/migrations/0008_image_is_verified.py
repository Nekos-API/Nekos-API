# Generated by Django 4.1.5 on 2023-02-01 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0007_alter_image_aspect_ratio"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="is_verified",
            field=models.BooleanField(
                default=False,
                help_text="Wether the image was verified by the staff or not.",
            ),
        ),
    ]
