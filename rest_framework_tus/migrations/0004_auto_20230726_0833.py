# Generated by Django 3.2.9 on 2023-07-26 08:33

import collections
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rest_framework_tus', '0003_auto_20170619_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='upload_metadata',
            field=jsonfield.fields.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict}),
        ),
    ]
