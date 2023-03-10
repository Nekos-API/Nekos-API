# Generated by Django 4.1.5 on 2023-02-09 05:09

from django.db import migrations, models
import dynamic_filenames


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="description",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="application",
            name="icon",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=dynamic_filenames.FilePattern(
                    filename_pattern="uploads/applications/icons"
                ),
            ),
        ),
    ]
