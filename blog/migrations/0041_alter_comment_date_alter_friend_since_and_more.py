# Generated by Django 4.2.3 on 2023-07-22 05:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0040_alter_comment_date_alter_friend_since_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 0, 40, 10, 236178)
            ),
        ),
        migrations.AlterField(
            model_name="friend",
            name="since",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 0, 40, 10, 236178)
            ),
        ),
        migrations.AlterField(
            model_name="friendrequest",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 0, 40, 10, 237180)
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 0, 40, 10, 237180)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 0, 40, 10, 236178)
            ),
        ),
    ]
