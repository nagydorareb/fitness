# Generated by Django 3.1.7 on 2021-04-12 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20210412_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='body_focus',
            field=models.CharField(blank=True, choices=[(None, 'All'), ('UP', 'Upper Body'), ('LW', 'Lower Body'), ('CR', 'Core'), ('TL', 'Total Body')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='training_type',
            field=models.CharField(blank=True, choices=[(None, 'All'), ('HI', 'HIIT'), ('ST', 'Strength Training'), ('YO', 'Yoga')], default=None, max_length=100, null=True),
        ),
    ]