# Generated by Django 5.0.6 on 2024-06-03 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("SortVision", "0003_kraj_created_date_kraj_publish_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="kraj",
            name="zdjecie",
            field=models.ImageField(
                blank=True,
                height_field=50,
                null=True,
                upload_to="images/",
                width_field=50,
            ),
        ),
    ]
