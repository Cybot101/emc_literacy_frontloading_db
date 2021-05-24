# Generated by Django 3.2.2 on 2021-05-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontloading', '0003_document_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='document',
            name='domains',
        ),
        migrations.AddField(
            model_name='document',
            name='domains',
            field=models.ManyToManyField(to='frontloading.Domain'),
        ),
        migrations.RemoveField(
            model_name='document',
            name='subjects',
        ),
        migrations.AddField(
            model_name='document',
            name='subjects',
            field=models.ManyToManyField(to='frontloading.Subject'),
        ),
        migrations.RemoveField(
            model_name='document',
            name='topics',
        ),
        migrations.AddField(
            model_name='document',
            name='topics',
            field=models.ManyToManyField(to='frontloading.Topic'),
        ),
        migrations.RemoveField(
            model_name='word',
            name='domains',
        ),
        migrations.AddField(
            model_name='word',
            name='domains',
            field=models.ManyToManyField(to='frontloading.Domain'),
        ),
        migrations.RemoveField(
            model_name='word',
            name='subjects',
        ),
        migrations.AddField(
            model_name='word',
            name='subjects',
            field=models.ManyToManyField(to='frontloading.Subject'),
        ),
        migrations.RemoveField(
            model_name='word',
            name='topics',
        ),
        migrations.AddField(
            model_name='word',
            name='topics',
            field=models.ManyToManyField(to='frontloading.Topic'),
        ),
    ]
