# Generated by Django 3.1.7 on 2021-03-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0006_auto_20210328_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]