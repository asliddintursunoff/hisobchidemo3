# Generated by Django 5.1.6 on 2025-03-07 22:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_alter_company_expiry_date_avans_jarima_premya'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avans',
            name='number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 22, 22, 58, 38, 12376, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='jarima',
            name='number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='premya',
            name='number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
