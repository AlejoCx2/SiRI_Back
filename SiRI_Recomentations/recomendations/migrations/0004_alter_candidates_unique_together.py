# Generated by Django 4.2 on 2023-05-28 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recomendations', '0003_alter_students_code'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candidates',
            unique_together={('idStudent', 'idVacancy')},
        ),
    ]
