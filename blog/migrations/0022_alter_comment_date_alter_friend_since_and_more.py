# Generated by Django 4.2.1 on 2023-05-31 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_comment_date_alter_post_date_friend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 31, 15, 17, 55, 507073)),
        ),
        migrations.AlterField(
            model_name='friend',
            name='since',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 31, 15, 17, 55, 507073)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 31, 15, 17, 55, 506073)),
        ),
    ]
