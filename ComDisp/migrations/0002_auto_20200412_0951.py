# Generated by Django 3.0.3 on 2020-04-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ComDisp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoinfo',
            name='channelId',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videoinfo',
            name='channelIdTitle',
            field=models.TextField(default='NA'),
            preserve_default=False,
        ),
    ]
