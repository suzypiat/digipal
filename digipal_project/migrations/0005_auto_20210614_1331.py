# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal', '0013_auto_20210427_1035'),
        ('digipal_project', '0004_auto_20210528_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonhum_ImageStoryCharacter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(to='digipal.Character')),
                ('image', models.ForeignKey(to='digipal.Image')),
                ('story_character', models.ForeignKey(verbose_name=b'character', to='digipal_project.Bonhum_StoryCharacter')),
            ],
            options={
                'verbose_name': 'image-character relationship',
                'verbose_name_plural': 'image-character relationships',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_MotiveStoryCharacter',
            fields=[
                ('allograph_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='digipal.Allograph')),
                ('story_character', models.ForeignKey(to='digipal_project.Bonhum_StoryCharacter')),
            ],
            bases=('digipal.allograph',),
        ),
        migrations.AlterModelOptions(
            name='bonhum_sourceauthor',
            options={'verbose_name': 'source-author relationship', 'verbose_name_plural': 'source-author relationships'},
        ),
        migrations.AlterModelOptions(
            name='bonhum_textcollaborator',
            options={'ordering': ['text'], 'verbose_name': 'text-collaborator relationship', 'verbose_name_plural': 'text-collaborator relationships'},
        ),
        migrations.AlterModelOptions(
            name='bonhum_textsource',
            options={'verbose_name': 'text-source relationship', 'verbose_name_plural': 'text-source relationships'},
        ),
        migrations.AlterModelOptions(
            name='bonhum_textstorycharacter',
            options={'verbose_name': 'text-character relationship', 'verbose_name_plural': 'text-character relationships'},
        ),
        migrations.AlterModelOptions(
            name='bonhum_workcurrentitem',
            options={'ordering': ['work', 'current_item'], 'verbose_name': 'current item-work relationship', 'verbose_name_plural': 'current item-work relationships'},
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='images',
            field=models.ManyToManyField(related_name='images_of_story_character', through='digipal_project.Bonhum_ImageStoryCharacter', to='digipal.Image'),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_imagestorycharacter',
            unique_together=set([('image', 'story_character', 'category')]),
        ),
    ]
