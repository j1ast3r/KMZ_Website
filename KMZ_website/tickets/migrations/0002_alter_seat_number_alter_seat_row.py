# Generated by Django 5.1rc1 on 2024-08-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='seat',
            name='row',
            field=models.IntegerField(default=1),
        ),
    ]