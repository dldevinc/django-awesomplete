# Generated by Django 3.1.2 on 2020-10-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201021_0805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='date',
        ),
        migrations.AddField(
            model_name='person',
            name='date',
            field=models.DateTimeField(blank=True, help_text="Select one of 'Yesterday', 'Today', 'Tomorrow'", null=True),
        ),
    ]
