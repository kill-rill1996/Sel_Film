# Generated by Django 3.2.9 on 2021-11-17 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('genres', models.CharField(blank=True, max_length=255, null=True)),
                ('countries', models.CharField(blank=True, max_length=400, null=True)),
                ('directors', models.CharField(blank=True, max_length=400, null=True)),
                ('actors', models.TextField(blank=True, null=True)),
                ('plot', models.TextField(blank=True, null=True)),
                ('rating', models.CharField(max_length=5)),
                ('image', models.ImageField(blank=True, null=True, upload_to='films/')),
            ],
        ),
    ]
