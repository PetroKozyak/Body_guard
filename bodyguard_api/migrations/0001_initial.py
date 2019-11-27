# Generated by Django 2.2.7 on 2019-11-14 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GuardFirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('comment', models.TextField(blank=True, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='guard_firm', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'guard_firm',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_job', models.IntegerField(choices=[(1, 'SOS'), (2, 'Regular order')], default=2)),
                ('title', models.CharField(max_length=50, null=True)),
                ('number_guard', models.IntegerField(blank=True, null=True)),
                ('start_time_guard', models.DateTimeField(null=True)),
                ('end_time_guard', models.DateTimeField(null=True)),
                ('type', models.IntegerField(choices=[(1, 'One time'), (2, 'Regular')], default=1, null=True)),
                ('coordinate', models.CharField(max_length=250, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jobs',
            },
        ),
        migrations.CreateModel(
            name='OptionGuard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'option',
            },
        ),
        migrations.CreateModel(
            name='VariantOptionGuard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='bodyguard_api.OptionGuard')),
            ],
            options={
                'db_table': 'variant',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('firm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='bodyguard_api.GuardFirm')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='bodyguard_api.Job')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='variant',
            field=models.ManyToManyField(blank=True, null=True, related_name='jobs', to='bodyguard_api.VariantOptionGuard'),
        ),
        migrations.CreateModel(
            name='FirmFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feed_backs', to=settings.AUTH_USER_MODEL)),
                ('firm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feed_backs', to='bodyguard_api.GuardFirm')),
            ],
            options={
                'db_table': 'feed_backs',
            },
        ),
    ]
