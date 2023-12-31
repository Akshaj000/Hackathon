# Generated by Django 4.2.4 on 2023-08-20 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hackathon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='hackathon/logo')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='hackathon/cover')),
                ('allowedSubmissionType', models.CharField(choices=[('image', 'Image'), ('file', 'File'), ('link', 'Link')], default='file', max_length=255)),
                ('minimumTeamSize', models.IntegerField(default=0)),
                ('maximumTeamSize', models.IntegerField(default=0)),
                ('allowIndividual', models.BooleanField(default=False)),
                ('startTimestamp', models.DateTimeField()),
                ('endTimestamp', models.DateTimeField()),
                ('pricePool', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Hackathon',
                'verbose_name_plural': 'Hackathons',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='hackathon/submission')),
                ('file', models.FileField(blank=True, null=True, upload_to='hackathon/submission')),
                ('link', models.URLField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('timestampSubmitted', models.DateTimeField(auto_now_add=True)),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.hackathon')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team.team')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Submission',
                'verbose_name_plural': 'Submissions',
                'unique_together': {('hackathon', 'team'), ('hackathon', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Organiser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.IntegerField(choices=[(0, 'admin'), (1, 'editor'), (2, 'viewer')], default=2)),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.hackathon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Organiser',
                'verbose_name_plural': 'Organisers',
                'unique_together': {('user', 'hackathon')},
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('timestampEvaluated', models.DateTimeField(auto_now_add=True)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.organiser')),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hackathon.submission')),
            ],
            options={
                'verbose_name': 'Evaluation',
                'verbose_name_plural': 'Evaluations',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestampRegistered', models.DateTimeField(auto_now_add=True)),
                ('meta', models.JSONField(default=dict)),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.hackathon')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team.team')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registration',
                'verbose_name_plural': 'Registrations',
                'unique_together': {('hackathon', 'team'), ('hackathon', 'user')},
            },
        ),
    ]
