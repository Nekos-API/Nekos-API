# Generated by Django 4.1.5 on 2023-02-09 05:16

from django.db import migrations
import django_resized.forms
import dynamic_filenames


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0002_alter_application_description_alter_application_icon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="icon",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=["middle", "center"],
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=100,
                scale=1,
                size=[1024, 1024],
                upload_to=dynamic_filenames.FilePattern(
                    filename_pattern="uploads/applications/icons/{uuid:base32}{ext}"
                ),
            ),
        ),
    ]
