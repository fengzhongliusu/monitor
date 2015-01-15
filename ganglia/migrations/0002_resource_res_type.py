# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ganglia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='res_type',
            field=models.CharField(default=b'hardware', max_length=200),
            preserve_default=True,
        ),
    ]
