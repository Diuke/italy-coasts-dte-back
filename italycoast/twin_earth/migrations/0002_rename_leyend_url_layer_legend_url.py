# Generated by Django 3.2.5 on 2021-10-29 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twin_earth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='layer',
            old_name='leyend_url',
            new_name='legend_url',
        ),
    ]
