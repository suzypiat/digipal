# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal', '0012_auto_20210415_0951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allograph',
            options={'ordering': ['character__ontograph__sort_order', 'character__ontograph__ontograph_type__name', 'name']},
        ),
        migrations.AlterModelOptions(
            name='allographcomponent',
            options={'ordering': ['allograph', 'component']},
        ),
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['ontograph__sort_order', 'ontograph__ontograph_type__name', 'name']},
        ),
        migrations.AlterModelOptions(
            name='characterform',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='idiograph',
            options={'ordering': ['allograph']},
        ),
        migrations.AlterModelOptions(
            name='ontograph',
            options={'ordering': ['sort_order', 'ontograph_type__name', 'name']},
        ),
        migrations.AlterModelOptions(
            name='ontographtype',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='scribe',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='text',
            options={'ordering': ['name'], 'verbose_name': 'Text Info', 'verbose_name_plural': 'Text Info'},
        ),
        migrations.AlterField(
            model_name='allograph',
            name='character',
            field=models.ForeignKey(to='digipal.Character'),
        ),
        migrations.AlterField(
            model_name='character',
            name='ontograph',
            field=models.ForeignKey(to='digipal.Ontograph'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='idiograph',
            field=models.ForeignKey(to='digipal.Idiograph'),
        ),
        migrations.AlterField(
            model_name='hand',
            name='scribe',
            field=models.ForeignKey(related_name='hands', to='digipal.Scribe', null=True),
        ),
        migrations.AlterField(
            model_name='idiograph',
            name='allograph',
            field=models.ForeignKey(to='digipal.Allograph'),
        ),
        migrations.AlterField(
            model_name='idiograph',
            name='scribe',
            field=models.ForeignKey(related_name='idiographs', blank=True, to='digipal.Scribe', null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_image', through='digipal_project.Bonhum_TextImage', to='digipal.Text'),
        ),
        migrations.AlterField(
            model_name='itempart',
            name='locus',
            field=models.CharField(default=b'face', max_length=64, null=True, help_text=b'The location of this part in the current item.', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='sources',
            field=models.ManyToManyField(related_name='sources_of_person', through='digipal_project.Bonhum_SourceAuthor', to='digipal_project.Bonhum_Source'),
        ),
        migrations.AlterField(
            model_name='scribe',
            name='scriptorium',
            field=models.ForeignKey(blank=True, to='digipal.Institution', null=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborators_of_text', through='digipal_project.Bonhum_TextCollaborator', to='digipal_project.Bonhum_Collaborator'),
        ),
        migrations.AlterField(
            model_name='text',
            name='images',
            field=models.ManyToManyField(related_name='images_of_text', through='digipal_project.Bonhum_TextImage', to='digipal.Image'),
        ),
        migrations.AlterField(
            model_name='text',
            name='reference',
            field=models.CharField(default=b'', max_length=30, verbose_name=b'canonical reference'),
        ),
        migrations.AlterField(
            model_name='text',
            name='sources',
            field=models.ManyToManyField(related_name='sources_of_text', through='digipal_project.Bonhum_TextSource', to='digipal_project.Bonhum_Source'),
        ),
        migrations.AlterField(
            model_name='text',
            name='story_characters',
            field=models.ManyToManyField(related_name='story_characters_of_text', through='digipal_project.Bonhum_TextStoryCharacter', to='digipal_project.Bonhum_StoryCharacter'),
        ),
        migrations.AlterUniqueTogether(
            name='text',
            unique_together=set([('name',)]),
        ),
    ]
