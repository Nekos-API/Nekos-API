from tortoise import migrations
from tortoise.migrations import operations as ops
from nanoid.generate import generate
from nekos_api.db.models.images import Rating
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Tag',
            fields=[
                ('id', fields.CharField(primary_key=True, default=generate, unique=True, db_index=True, max_length=21)),
                ('name', fields.CharField(unique=True, max_length=50)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
            ],
            options={'table': 'tag', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Image',
            fields=[
                ('id', fields.CharField(primary_key=True, default=generate, unique=True, db_index=True, max_length=21)),
                ('url', fields.CharField(max_length=2048)),
                ('rating', fields.CharEnumField(description='SAFE: safe\nSUGGESTIVE: suggestive\nBORDERLINE: borderline\nEXPLICIT: explicit', enum_type=Rating, max_length=10)),
                ('color_primary', fields.CharField(null=True, max_length=7)),
                ('color_palette', fields.CharField(null=True, max_length=79)),
                ('artist_name', fields.CharField(null=True, max_length=100)),
                ('source_id', fields.CharField(null=True, max_length=100)),
                ('source_url', fields.CharField(null=True, max_length=255)),
                ('tags', fields.ManyToManyField('models.Tag', unique=True, db_constraint=True, through='image_tag', forward_key='tag_id', backward_key='image_id', related_name='images', on_delete=OnDelete.CASCADE)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
            ],
            options={'table': 'image', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
