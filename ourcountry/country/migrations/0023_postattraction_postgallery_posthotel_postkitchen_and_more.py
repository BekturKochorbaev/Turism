# Generated by Django 5.1.4 on 2025-03-02 06:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0022_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAttraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='country.attractionreview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attractions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'post')},
            },
        ),
        migrations.CreateModel(
            name='PostGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now=True)),
                ('post_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_gallery', to='country.galleryreview')),
                ('user_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_gallery', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_gallery', 'post_gallery')},
            },
        ),
        migrations.CreateModel(
            name='PostHotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now=True)),
                ('post_hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_hotel', to='country.hotelsreview')),
                ('user_hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_hotel', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_hotel', 'post_hotel')},
            },
        ),
        migrations.CreateModel(
            name='PostKitchen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now=True)),
                ('post_kitchen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_kitchen', to='country.kitchenreview')),
                ('user_kitchen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_kitchen', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_kitchen', 'post_kitchen')},
            },
        ),
        migrations.CreateModel(
            name='PostPopular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now=True)),
                ('post_popular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_popular', to='country.popularreview')),
                ('user_popular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_popular', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_popular', 'post_popular')},
            },
        ),
    ]
