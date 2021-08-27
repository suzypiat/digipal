# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal', '0016_auto_20210621_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestlog',
            name='request',
            field=models.CharField(default=b'', max_length=600, null=True, blank=True),
        ),
    ]
