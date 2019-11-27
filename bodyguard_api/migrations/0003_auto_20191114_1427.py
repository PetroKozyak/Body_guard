# Generated by Django 2.2.7 on 2019-11-14 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bodyguard_api', '0002_auto_20191114_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='bodyguard_api.Role'),
        ),
    ]
