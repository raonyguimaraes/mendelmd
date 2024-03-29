# Generated by Django 4.2.6 on 2023-10-25 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0001_initial'),
        ('projects', '0002_project_samples'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('samples', '0003_alter_sample_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('repository', models.CharField(blank=True, max_length=600, null=True)),
            ],
            options={
                'verbose_name_plural': 'analysis_types',
            },
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('params', models.JSONField(blank=True, null=True)),
                ('name', models.CharField(max_length=30)),
                ('status', models.TextField(blank=True, null=True)),
                ('files', models.ManyToManyField(to='files.file')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('samples', models.ManyToManyField(to='samples.sample')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'analyses',
            },
        ),
    ]
