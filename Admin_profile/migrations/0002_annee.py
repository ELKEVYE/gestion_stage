# Generated by Django 5.0.5 on 2025-02-08 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'annee',
            },
        ),
    ]
