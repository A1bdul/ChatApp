# Generated by Django 4.2.5 on 2023-10-03 01:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]