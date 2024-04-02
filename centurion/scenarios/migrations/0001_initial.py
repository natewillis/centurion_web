# Generated by Django 5.0.3 on 2024-04-01 20:37

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('offset', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exercise_start_datetime', models.DateTimeField()),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Pickup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset', models.DurationField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('altitude_ft', models.FloatField()),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.box')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pickups', to='scenarios.order')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('offset', models.DurationField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('altitude_ft', models.FloatField()),
                ('pickup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='scenarios.pickup')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='scenario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='scenarios.scenario'),
        ),
    ]