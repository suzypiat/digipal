# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal_project', '0003_auto_20210504_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonhum_source',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_textsource',
            unique_together=set([('source', 'text', 'canonical_reference')]),
        ),
    ]
