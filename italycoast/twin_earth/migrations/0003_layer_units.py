# Generated by Django 3.2.5 on 2022-02-08 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twin_earth', '0002_rename_leyend_url_layer_legend_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='units',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
