# Generated by Django 3.1 on 2020-09-02 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ozi', '0011_auto_20200902_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='repeat',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
