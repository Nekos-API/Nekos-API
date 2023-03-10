# Generated by Django 4.1.5 on 2023-02-19 05:33

from django.db import migrations
import django_resized.forms
import dynamic_filenames


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0017_githubuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar_image",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=["middle", "center"],
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=100,
                scale=1,
                size=[512, 512],
                upload_to=dynamic_filenames.FilePattern(
                    filename_pattern="uploads/user/avatar/{uuid:base32}{ext}"
                ),
            ),
        ),
    ]
