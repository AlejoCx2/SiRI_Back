# Generated by Django 4.2 on 2023-05-23 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recomendations', '0002_candidates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='code',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
