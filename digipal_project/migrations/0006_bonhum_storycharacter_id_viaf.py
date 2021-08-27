# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal_project', '0005_auto_20210614_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='id_viaf',
            field=models.IntegerField(null=True, verbose_name=b'VIAF identifier', blank=True),
        ),
    ]
