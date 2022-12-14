# Generated by Django 4.1 on 2022-09-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_remove_results_results_id_alter_studies_study_design'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studies',
            name='Study_design',
            field=models.CharField(blank=True, choices=[('CS', 'Case series'), ('CST', 'Cross-sectional'), ('P', 'Prospective'), ('PRP', 'Prospective and Retrospective'), ('PC', 'Prospective cohort'), ('R', 'Report'), ('RP', 'Retrospective'), ('RPR', 'Retrospective review'), ('RPC', 'Retrospective cohort'), ('RA', 'Review article'), ('O', 'Other')], max_length=3),
        ),
        migrations.AlterField(
            model_name='studies',
            name='Study_group',
            field=models.CharField(blank=True, choices=[('SST', 'Superficial skin and throat'), ('IG', 'Invasive GAS'), ('ARF', 'ARF'), ('ASPGN', 'APSGN')], max_length=5),
        ),
    ]
