# Generated by Django 3.2 on 2021-04-21 07:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrent',
            name='created',
            field=models.DateField(default=datetime.date(2021, 4, 21)),
        ),
        migrations.AlterField(
            model_name='bookrent',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
