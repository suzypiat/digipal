# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('digipal_project', '0001_initial'),
        ('digipal', '0011_auto_20201004_2014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allograph',
            options={'ordering': ['character__ontograph__sort_order', 'character__ontograph__ontograph_type__name', 'name'], 'verbose_name': 'motive', 'verbose_name_plural': 'motives'},
        ),
        migrations.AlterModelOptions(
            name='allographcomponent',
            options={'ordering': ['allograph', 'component'], 'verbose_name': 'motive component', 'verbose_name_plural': 'motive components'},
        ),
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['ontograph__sort_order', 'ontograph__ontograph_type__name', 'name'], 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='characterform',
            options={'ordering': ['name'], 'verbose_name': 'category form', 'verbose_name_plural': 'category forms'},
        ),
        migrations.AlterModelOptions(
            name='idiograph',
            options={'ordering': ['allograph'], 'verbose_name': 'attribution', 'verbose_name_plural': 'attributions'},
        ),
        migrations.AlterModelOptions(
            name='ontograph',
            options={'ordering': ['sort_order', 'ontograph_type__name', 'name'], 'verbose_name': 'macro category', 'verbose_name_plural': 'macro categories'},
        ),
        migrations.AlterModelOptions(
            name='ontographtype',
            options={'ordering': ['name'], 'verbose_name': 'macro category type', 'verbose_name_plural': 'macro category types'},
        ),
        migrations.AlterModelOptions(
            name='scribe',
            options={'ordering': ['type', 'name'], 'verbose_name': 'contributor', 'verbose_name_plural': 'contributors'},
        ),
        migrations.AlterModelOptions(
            name='text',
            options={'ordering': ['title'], 'verbose_name': 'text', 'verbose_name_plural': 'texts'},
        ),
        migrations.AddField(
            model_name='characterform',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 15, 8, 51, 15, 270891, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='characterform',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 15, 8, 51, 22, 35394, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currentitem',
            name='works',
            field=models.ManyToManyField(related_name='works_of_current_item', through='digipal_project.Bonhum_WorkCurrentItem', to='digipal_project.Bonhum_Work'),
        ),
        migrations.AddField(
            model_name='image',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_image', through='digipal_project.Bonhum_TextImage', to='digipal.Text', blank=True),
        ),
        migrations.AddField(
            model_name='itempart',
            name='work_current_item',
            field=models.ForeignKey(verbose_name=b'current item/work', to='digipal_project.Bonhum_WorkCurrentItem', null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='sources',
            field=models.ManyToManyField(related_name='sources', through='digipal_project.Bonhum_SourceAuthor', to='digipal_project.Bonhum_Source', blank=True),
        ),
        migrations.AddField(
            model_name='scribe',
            name='type',
            field=models.ForeignKey(to='digipal_project.Bonhum_ContributorType', null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborators_of_text', through='digipal_project.Bonhum_TextCollaborator', to='digipal_project.Bonhum_Collaborator', blank=True),
        ),
        migrations.AddField(
            model_name='text',
            name='edition',
            field=models.ForeignKey(default=None, blank=True, to='digipal_project.Bonhum_Edition', help_text=b'Please select either an item part or an edition.', null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='images',
            field=models.ManyToManyField(related_name='images_of_text', through='digipal_project.Bonhum_TextImage', to='digipal.Image', blank=True),
        ),
        migrations.AddField(
            model_name='text',
            name='item_part',
            field=models.ForeignKey(default=None, blank=True, to='digipal.ItemPart', help_text=b'Please select either an item part or an edition.', null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mythological',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='text',
            name='reference',
            field=models.CharField(default=b'', unique=True, max_length=30, verbose_name=b'canonical reference'),
        ),
        migrations.AddField(
            model_name='text',
            name='sources',
            field=models.ManyToManyField(related_name='sources_of_text', through='digipal_project.Bonhum_TextSource', to='digipal_project.Bonhum_Source', blank=True),
        ),
        migrations.AddField(
            model_name='text',
            name='story_characters',
            field=models.ManyToManyField(related_name='story_characters_of_text', through='digipal_project.Bonhum_TextStoryCharacter', to='digipal_project.Bonhum_StoryCharacter', blank=True),
        ),
        migrations.AddField(
            model_name='text',
            name='story_place',
            field=models.ForeignKey(default=None, blank=True, to='digipal_project.Bonhum_StoryPlace', null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='story_start_date',
            field=models.CharField(help_text=b'Only if the story is not mythological.', max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='text',
            name='title',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='text',
            name='type',
            field=models.ForeignKey(to='digipal_project.Bonhum_TextType', null=True),
        ),
        migrations.AlterField(
            model_name='allograph',
            name='character',
            field=models.ForeignKey(verbose_name=b'category', to='digipal.Character'),
        ),
        migrations.AlterField(
            model_name='allograph',
            name='hidden',
            field=models.BooleanField(default=False, help_text="If ticked the public users won't see this motive on the web site."),
        ),
        migrations.AlterField(
            model_name='character',
            name='ontograph',
            field=models.ForeignKey(verbose_name=b'macro category', to='digipal.Ontograph'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='idiograph',
            field=models.ForeignKey(verbose_name=b'attribution', to='digipal.Idiograph'),
        ),
        migrations.AlterField(
            model_name='hand',
            name='scribe',
            field=models.ForeignKey(related_name='hands', verbose_name=b'contributor', to='digipal.Scribe', null=True),
        ),
        migrations.AlterField(
            model_name='idiograph',
            name='allograph',
            field=models.ForeignKey(verbose_name=b'motive', to='digipal.Allograph'),
        ),
        migrations.AlterField(
            model_name='idiograph',
            name='scribe',
            field=models.ForeignKey(related_name='idiographs', verbose_name=b'contributor', blank=True, to='digipal.Scribe', null=True),
        ),
        migrations.AlterField(
            model_name='itempart',
            name='locus',
            field=models.CharField(default=b'face', max_length=64, null=True, help_text=b'The location of this part in the current item', blank=True),
        ),
        migrations.AlterField(
            model_name='ontograph',
            name='nesting_level',
            field=models.IntegerField(default=0, help_text=b'A macro category can contain another macro category of a higher level. E.g. level 3 con be made of macro categories of level 4 and above. Set 0 to prevent any nesting.'),
        ),
        migrations.AlterField(
            model_name='scribe',
            name='scriptorium',
            field=models.ForeignKey(verbose_name=b'workshop', blank=True, to='digipal.Institution', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='text',
            unique_together=set([]),
        ),
    ]
