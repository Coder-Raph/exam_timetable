# Generated by Django 5.0.1 on 2024-03-11 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedTimetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='generated_timetables/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
