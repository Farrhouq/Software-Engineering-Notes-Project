# Generated by Django 5.0.6 on 2024-07-24 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_label_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='favorite',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
