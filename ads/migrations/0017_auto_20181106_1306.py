# Generated by Django 2.1.2 on 2018-11-06 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0016_adimage_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adimage',
            name='device',
            field=models.CharField(default='All devices', max_length=2, verbose_name='Device'),
        ),
    ]
