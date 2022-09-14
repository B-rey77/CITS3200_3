# Generated by Django 4.1 on 2022-09-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_alter_studies_study_design_alter_studies_study_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='Age_general',
            field=models.CharField(blank=True, choices=[('ALL', 'All ages'), ('AD', 'Adult'), ('C', 'Children'), ('AL', 'Adolescents'), ('I', 'Infant'), ('M', 'Mix')], max_length=5),
        ),
    ]
