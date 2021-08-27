# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal', '0014_image_story_characters'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='id_viaf',
            field=models.IntegerField(null=True, verbose_name=b'VIAF identifier', blank=True),
        ),
    ]
