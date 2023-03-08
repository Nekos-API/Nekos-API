# Generated by Django 4.1.5 on 2023-03-08 18:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0015_imagesourceresult_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="imagesourceresult",
            name="result",
        ),
        migrations.AddField(
            model_name="imagesourceresult",
            name="artist_name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="imagesourceresult",
            name="artist_url",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="imagesourceresult",
            name="ext_urls",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.URLField(max_length=500),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="imagesourceresult",
            name="similarity",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="imagesourceresult",
            name="title",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="imagesourceresult",
            name="source",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]