# Generated by Django 4.2.10 on 2024-02-29 16:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addcorpus', '0008_alter_field_display_type_geo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='visualizations',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('resultscount', 'Number of results'), ('termfrequency', 'Frequency of the search term'), (
                'ngram', 'Neighbouring words'), ('wordcloud', 'Most frequent words'), ('map', 'Map of geo-coordinates')], max_length=16), blank=True, default=list, help_text='visualisations for this field', size=None),
        ),
    ]
