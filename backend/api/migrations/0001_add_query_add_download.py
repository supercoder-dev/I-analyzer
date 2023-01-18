# Generated by Django 4.1.5 on 2023-01-11 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addcorpus', '0001_add_corpus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_json', models.JSONField()),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('completed', models.DateTimeField(null=True)),
                ('aborted', models.BooleanField(null=True)),
                ('transferred', models.BigIntegerField(null=True)),
                ('total_results', models.BigIntegerField(null=True)),
                ('corpus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries', to='addcorpus.corpus', to_field='name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Queries',
            },
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('completed', models.DateTimeField(null=True)),
                ('download_type', models.CharField(max_length=126)),
                ('parameters', models.JSONField()),
                ('filename', models.FilePathField(max_length=254, null=True, path='/home/luka/Documents/I-analyzer/I-analyzer-django/backend/ianalyzer/../api/csv_files')),
                ('corpus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downloads', to='addcorpus.corpus', to_field='name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downloads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
