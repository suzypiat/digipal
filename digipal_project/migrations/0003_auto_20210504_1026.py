# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal_project', '0002_auto_20210427_1036'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bonhum_storycharacternamevariant',
            unique_together=set([('name', 'character', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_storyplacenamevariant',
            unique_together=set([('name', 'place', 'language')]),
        ),
    ]
