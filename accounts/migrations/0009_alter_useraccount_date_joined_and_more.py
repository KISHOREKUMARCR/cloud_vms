# Generated by Django 4.2 on 2024-06-06 16:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_useraccount_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 6, 11, 4, 40, 825835, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 6, 11, 4, 40, 825835, tzinfo=datetime.timezone.utc)),
        ),
    ]