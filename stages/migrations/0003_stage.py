# Generated by Django 5.0.5 on 2025-02-09 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_profile', '0002_annee'),
        ('stages', '0002_encadrant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('annee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_profile.annee')),
                ('encadrants', models.ManyToManyField(related_name='stages', to='stages.encadrant')),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stages.entreprise')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_profile.etudiant')),
            ],
            options={
                'db_table': 'stage',
            },
        ),
    ]
