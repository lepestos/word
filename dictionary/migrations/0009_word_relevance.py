# Generated by Django 3.1.7 on 2021-04-02 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0008_auto_20210328_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='relevance',
            field=models.DecimalField(decimal_places=3, default=1000.0, max_digits=7),
        ),
    ]
