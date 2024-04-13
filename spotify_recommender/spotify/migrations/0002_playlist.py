# Generated by Django 5.0.4 on 2024-04-12 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('playlist_id', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('playlist_name', models.TextField(max_length=100)),
                ('playlist_url', models.CharField(max_length=1000)),
                ('playlist_num_tracks', models.IntegerField(null=True)),
                ('playlist_featured', models.BooleanField(default=False)),
                ('playlist_owner', models.CharField(max_length=500)),
                ('date_created', models.CharField(default='No date', max_length=500)),
                ('playlist_img_src', models.CharField(default='no_img', max_length=5000, null=True)),
            ],
        ),
    ]