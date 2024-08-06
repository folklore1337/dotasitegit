# Generated by Django 5.0.7 on 2024-07-13 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dotasiteview', '0002_menuitem_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkinsItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название скина')),
                ('image', models.ImageField(upload_to='images', verbose_name='Изображение скина')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Ссылка на стим')),
                ('link_1', models.URLField(blank=True, null=True, verbose_name='Ссылка на лис-скинс')),
                ('type', models.CharField(choices=[('IMO', 'Immortal'), ('ARC', 'Arcana')], default='IMO', max_length=3, verbose_name='Редкость')),
            ],
        ),
    ]
