# Generated by Django 3.1 on 2020-09-02 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ozi', '0009_update_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
