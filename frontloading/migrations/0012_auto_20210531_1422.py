# Generated by Django 3.2.2 on 2021-05-31 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontloading', '0011_rename_image_ref_word_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
    ]