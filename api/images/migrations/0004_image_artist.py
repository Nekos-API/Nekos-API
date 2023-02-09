# Generated by Django 4.1.5 on 2023-01-26 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("artists", "0001_initial"),
        ("images", "0003_image_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="artist",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="artists.artist",
            ),
        ),
    ]