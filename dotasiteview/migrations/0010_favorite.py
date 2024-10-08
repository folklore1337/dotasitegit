# Generated by Django 5.0.7 on 2024-07-19 02:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dotasiteview', '0009_alter_skinsitem_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skins_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dotasiteview.skinsitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('weather_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dotasiteview.weatheritem')),
            ],
            options={
                'unique_together': {('user', 'skins_item', 'weather_item')},
            },
        ),
    ]
