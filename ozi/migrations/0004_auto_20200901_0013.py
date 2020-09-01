# Generated by Django 3.1 on 2020-09-01 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ozi', '0003_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='subscriptions',
            field=models.ManyToManyField(to='ozi.Mailing'),
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('bot', 'chat')},
        ),
    ]
