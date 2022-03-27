# Generated by Django 3.2.5 on 2022-03-26 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twin_earth', '0007_alter_layer_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('scenario_json', models.JSONField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scenarios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Scenario',
                'verbose_name_plural': 'Scenarios',
                'db_table': 'scenario',
            },
        ),
    ]