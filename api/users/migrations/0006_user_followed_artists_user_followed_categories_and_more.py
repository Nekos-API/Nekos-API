# Generated by Django 4.1.5 on 2023-01-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_alter_category_options_alter_category_is_nsfw"),
        ("artists", "0002_alter_artist_image_alter_artist_links"),
        ("characters", "0004_alter_character_gender"),
        ("users", "0005_remove_user_favorite_images_user_liked_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="followed_artists",
            field=models.ManyToManyField(related_name="followers", to="artists.artist"),
        ),
        migrations.AddField(
            model_name="user",
            name="followed_categories",
            field=models.ManyToManyField(
                related_name="followers", to="categories.category"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="followed_characters",
            field=models.ManyToManyField(
                related_name="followers", to="characters.character"
            ),
        ),
    ]
