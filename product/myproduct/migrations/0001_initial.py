# Generated by Django 3.1.7 on 2021-02-23 09:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('logo', models.ImageField(upload_to='product/')),
                ('rotate_duration', models.FloatField()),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(blank=True, default='', null=True)),
            ],
        ),
    ]
