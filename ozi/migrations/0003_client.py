# Generated by Django 3.1 on 2020-09-01 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ozi", "0002_auto_20200901_0001"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bot", models.CharField(max_length=50)),
                ("chat", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name": "client",
                "verbose_name_plural": "clients",
            },
        ),
    ]