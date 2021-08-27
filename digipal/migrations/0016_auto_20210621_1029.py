# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal', '0015_person_id_viaf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='display_label',
            field=models.CharField(max_length=600, editable=False),
        ),
        migrations.AlterField(
            model_name='idiograph',
            name='display_label',
            field=models.CharField(max_length=518, editable=False),
        ),
    ]
