# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal_project', '0005_auto_20210614_1331'),
        ('digipal', '0013_auto_20210427_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='story_characters',
            field=models.ManyToManyField(related_name='story_characters_of_image', through='digipal_project.Bonhum_ImageStoryCharacter', to='digipal_project.Bonhum_StoryCharacter'),
        ),
    ]
