# Generated by Django 4.2.3 on 2023-07-23 04:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("song", "0005_artiststats_alter_song_date"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ArtistStats",
            new_name="ArtistStat",
        ),
        migrations.AlterField(
            model_name="song",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 22, 23, 58, 17, 135388)
            ),
        ),
    ]
