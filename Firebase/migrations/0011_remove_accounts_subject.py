# Generated by Django 2.0.7 on 2018-08-04 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Firebase', '0010_accounts_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='subject',
        ),
    ]
