# Generated by Django 5.1.6 on 2025-03-01 22:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_progress_type_work_types_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 16, 22, 31, 51, 810478, tzinfo=datetime.timezone.utc)),
        ),
    ]
