# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal_project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonhum_collaborator',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='bonhum_collaborator',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='bonhum_collaborator',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_collaborator', through='digipal_project.Bonhum_TextCollaborator', to='digipal.Text'),
        ),
        migrations.AlterField(
            model_name='bonhum_source',
            name='authors',
            field=models.ManyToManyField(related_name='authors_of_source', through='digipal_project.Bonhum_SourceAuthor', to='digipal.Person'),
        ),
        migrations.AlterField(
            model_name='bonhum_source',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_source', through='digipal_project.Bonhum_TextSource', to='digipal.Text'),
        ),
        migrations.AlterField(
            model_name='bonhum_storycharacter',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_story_character', through='digipal_project.Bonhum_TextStoryCharacter', to='digipal.Text'),
        ),
        migrations.AlterField(
            model_name='bonhum_storycharacternamevariant',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='bonhum_storyplace',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='bonhum_storyplacenamevariant',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='bonhum_work',
            name='current_items',
            field=models.ManyToManyField(related_name='current_items_of_work', through='digipal_project.Bonhum_WorkCurrentItem', to='digipal.CurrentItem'),
        ),
        migrations.AlterField(
            model_name='bonhum_work',
            name='date',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='bonhum_work',
            name='title',
            field=models.TextField(),
        ),
    ]
