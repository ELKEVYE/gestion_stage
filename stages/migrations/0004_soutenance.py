# Generated by Django 5.0.5 on 2025-02-10 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0003_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Soutenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_soutenance', models.DateField()),
                ('note', models.DecimalField(decimal_places=2, max_digits=4)),
                ('commentaire', models.TextField(blank=True)),
                ('stage', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stages.stage')),
            ],
        ),
    ]
