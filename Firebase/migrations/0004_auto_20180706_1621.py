# Generated by Django 2.0.6 on 2018-07-06 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Firebase', '0003_auto_20180706_1615'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizes',
            old_name='section',
            new_name='sections',
        ),
        migrations.RenameField(
            model_name='quizes',
            old_name='subject',
            new_name='subjects',
        ),
    ]
