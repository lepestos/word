# Generated by Django 3.1.7 on 2021-03-27 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_auto_20210326_1452'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ('-timestamp',)},
        ),
    ]