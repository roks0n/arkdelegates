# Generated by Django 2.2 on 2019-05-20 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20190324_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusupdate',
            name='title',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]