# Generated by Django 5.1.6 on 2025-03-11 22:42

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_remove_expanse_number_expanse_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 26, 22, 42, 58, 873548, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='dateforexpanse',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
