# Generated by Django 3.0.3 on 2020-04-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ComDisp', '0002_auto_20200412_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoinfo',
            name='videoId',
            field=models.TextField(default='NA'),
            preserve_default=False,
        ),
    ]
