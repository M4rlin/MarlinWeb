# Generated by Django 2.0.6 on 2018-07-01 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Firebase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizes',
            name='Quiz_Date',
            field=models.CharField(max_length=20),
        ),
    ]
