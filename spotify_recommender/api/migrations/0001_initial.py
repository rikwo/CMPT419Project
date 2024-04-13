# Generated by Django 5.0.4 on 2024-04-11 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=8, unique=True)),
                ('user', models.CharField(max_length=50, unique=True)),
                ('popularity', models.IntegerField(default=5)),
                ('danceability', models.IntegerField(default=5)),
                ('energy', models.IntegerField(default=5)),
                ('valence', models.IntegerField(default=5)),
                ('tempo', models.IntegerField(default=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
