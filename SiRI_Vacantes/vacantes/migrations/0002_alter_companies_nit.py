# Generated by Django 4.2 on 2023-04-26 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='nit',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
