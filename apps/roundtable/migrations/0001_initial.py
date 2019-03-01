# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-01 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('message', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=400)),
                ('display_phone', models.CharField(max_length=45)),
                ('review_count', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('display_address', models.TextField()),
                ('photo1_url', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('photo2_url', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('photo3_url', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('price', models.CharField(blank=True, default='', max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('events', models.ManyToManyField(related_name='restaurants', to='roundtable.Event')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='rater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='roundtable.User'),
        ),
        migrations.AddField(
            model_name='rating',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='roundtable.Restaurant'),
        ),
        migrations.AddField(
            model_name='event',
            name='hosted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_events', to='roundtable.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='users_who_join',
            field=models.ManyToManyField(related_name='join_events', to='roundtable.User'),
        ),
    ]
