# Generated by Django 5.1.4 on 2025-03-11 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0052_rename_kitchen_region_kitchenreview_kitchen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotelsreview',
            old_name='created_date',
            new_name='created_at',
        ),
    ]
