# Generated by Django 4.2.6 on 2024-01-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0012_alter_tag_danbooru_tags_alter_tag_id_v2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='rating',
            field=models.CharField(blank=True, choices=[('safe', 'Safe'), ('suggestive', 'Suggestive'), ('borderline', 'Borderline'), ('explicit', 'Explicit')], max_length=12, null=True),
        ),
    ]
