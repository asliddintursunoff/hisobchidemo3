# Generated by Django 5.1.6 on 2025-03-07 19:32

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_alter_company_expiry_date_workerexpanses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 22, 19, 32, 24, 409683, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Avans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Jarima',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Premya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.worker')),
            ],
        ),
    ]
