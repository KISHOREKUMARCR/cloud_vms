# Generated by Django 4.1 on 2024-05-24 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vfms', '0002_alter_videofiles_videofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudURI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('project_name', models.CharField(max_length=255)),
                ('location_name', models.CharField(max_length=255)),
                ('video_start_time', models.DateTimeField()),
                ('video_end_time', models.DateTimeField()),
                ('cloud_uri', models.URLField()),
            ],
        ),
    ]
