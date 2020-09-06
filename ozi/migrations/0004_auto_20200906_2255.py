# Generated by Django 3.1 on 2020-09-06 22:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ozi', '0003_mailing_common'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hook',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='update',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
