# Generated by Django 4.2.3 on 2023-07-23 04:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0042_alter_comment_date_alter_friend_since_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 23, 53, 26, 759208)
            ),
        ),
        migrations.AlterField(
            model_name="friend",
            name="since",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 23, 53, 26, 759208)
            ),
        ),
        migrations.AlterField(
            model_name="friendrequest",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 23, 53, 26, 759208)
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 23, 53, 26, 759208)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 23, 53, 26, 758208)
            ),
        ),
    ]
