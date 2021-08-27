# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal', '0011_auto_20201004_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonhum_Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_Catalogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reference', models.TextField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('current_item', models.ForeignKey(to='digipal.CurrentItem')),
            ],
            options={
                'ordering': ['current_item', 'reference'],
                'verbose_name': 'catalogue',
                'verbose_name_plural': 'catalogues',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_Collaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(unique=True, max_length=150)),
                ('last_name', models.CharField(unique=True, max_length=150)),
                ('institution', models.CharField(max_length=150)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'verbose_name': 'collaborator',
                'verbose_name_plural': 'collaborators',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_ContributorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'contributor type',
                'verbose_name_plural': 'contributor types',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_Edition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(unique=True)),
                ('date', models.CharField(max_length=30)),
                ('publisher', models.CharField(max_length=100)),
                ('complete_work', models.BooleanField(default=False)),
                ('work_title', models.TextField(help_text=b'If the work name is different in this edition.', null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('editor', models.ForeignKey(to='digipal.Person')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'edition',
                'verbose_name_plural': 'editions',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(unique=True)),
                ('reference', models.TextField(unique=True, verbose_name=b'canonical reference')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'source',
                'verbose_name_plural': 'sources',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_SourceAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to='digipal.Person')),
                ('source', models.ForeignKey(to='digipal_project.Bonhum_Source')),
            ],
        ),
        migrations.CreateModel(
            name='Bonhum_SourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'source type',
                'verbose_name_plural': 'source types',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character',
                'verbose_name_plural': 'characters',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterAge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character age',
                'verbose_name_plural': 'character ages',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterGender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character gender',
                'verbose_name_plural': 'character genders',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterNameVariant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('character', models.ForeignKey(to='digipal_project.Bonhum_StoryCharacter')),
                ('language', models.ForeignKey(to='digipal.Language')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character name variant',
                'verbose_name_plural': 'character name variants',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterOccupation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character occupation',
                'verbose_name_plural': 'character occupations',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterReligion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character religion',
                'verbose_name_plural': 'character religions',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character title',
                'verbose_name_plural': 'character titles',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterTrait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character trait',
                'verbose_name_plural': 'character traits',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryCharacterType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'character type',
                'verbose_name_plural': 'character types',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryPlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'story place',
                'verbose_name_plural': 'story places',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryPlaceNameVariant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('language', models.ForeignKey(to='digipal.Language')),
                ('place', models.ForeignKey(to='digipal_project.Bonhum_StoryPlace')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'story place name variant',
                'verbose_name_plural': 'story place name variants',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryPlaceNature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'story place nature',
                'verbose_name_plural': 'story place natures',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_StoryPlaceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('level', models.IntegerField(default=0, help_text=b'The level of this story place type:<br/>0 means a country, a river, an ocean, a mountain or a mythological place<br/>1 means a region<br/>2 means a city', choices=[(0, b'0'), (1, b'1'), (2, b'2')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['level', 'name'],
                'verbose_name': 'story place type',
                'verbose_name_plural': 'story place types',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_TextCollaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(to='digipal_project.Bonhum_Activity')),
                ('collaborator', models.ForeignKey(to='digipal_project.Bonhum_Collaborator')),
                ('text', models.ForeignKey(to='digipal.Text')),
            ],
            options={
                'ordering': ['text'],
                'verbose_name': 'Text/collaborator relationship',
                'verbose_name_plural': 'Text/collaborator relationships',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_TextImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(to='digipal.Image')),
                ('text', models.ForeignKey(to='digipal.Text')),
            ],
        ),
        migrations.CreateModel(
            name='Bonhum_TextSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('canonical_reference', models.CharField(max_length=25, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(to='digipal_project.Bonhum_Source')),
                ('text', models.ForeignKey(to='digipal.Text')),
            ],
        ),
        migrations.CreateModel(
            name='Bonhum_TextStoryCharacter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('story_character', models.ForeignKey(to='digipal_project.Bonhum_StoryCharacter')),
                ('text', models.ForeignKey(to='digipal.Text')),
            ],
        ),
        migrations.CreateModel(
            name='Bonhum_TextType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'text type',
                'verbose_name_plural': 'text types',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(unique=True)),
                ('date', models.CharField(unique=True, max_length=30)),
                ('original_version', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'work',
                'verbose_name_plural': 'works',
            },
        ),
        migrations.CreateModel(
            name='Bonhum_WorkCurrentItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complete_work', models.BooleanField(default=False)),
                ('work_title', models.TextField(help_text=b'If the work name is different in this current item.', null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('current_item', models.ForeignKey(to='digipal.CurrentItem')),
                ('work', models.ForeignKey(to='digipal_project.Bonhum_Work')),
            ],
            options={
                'ordering': ['work', 'current_item'],
                'verbose_name': 'Current item/work relationship',
                'verbose_name_plural': 'Current item/work relationships',
            },
        ),
        migrations.AddField(
            model_name='bonhum_work',
            name='current_items',
            field=models.ManyToManyField(related_name='current_items_of_work', through='digipal_project.Bonhum_WorkCurrentItem', to='digipal.CurrentItem', blank=True),
        ),
        migrations.AddField(
            model_name='bonhum_work',
            name='language',
            field=models.ForeignKey(to='digipal.Language'),
        ),
        migrations.AddField(
            model_name='bonhum_work',
            name='translator',
            field=models.ForeignKey(blank=True, to='digipal.Person', help_text=b'A translator must be selected if it is not an original version.', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_storyplacetype',
            unique_together=set([('name', 'level')]),
        ),
        migrations.AddField(
            model_name='bonhum_storyplace',
            name='nature',
            field=models.ForeignKey(to='digipal_project.Bonhum_StoryPlaceNature'),
        ),
        migrations.AddField(
            model_name='bonhum_storyplace',
            name='parent',
            field=models.ForeignKey(blank=True, to='digipal_project.Bonhum_StoryPlace', null=True),
        ),
        migrations.AddField(
            model_name='bonhum_storyplace',
            name='type',
            field=models.ForeignKey(to='digipal_project.Bonhum_StoryPlaceType'),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='age',
            field=models.ForeignKey(blank=True, to='digipal_project.Bonhum_StoryCharacterAge', null=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='gender',
            field=models.ForeignKey(blank=True, to='digipal_project.Bonhum_StoryCharacterGender', null=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='geographical_origin',
            field=models.ForeignKey(blank=True, to='digipal_project.Bonhum_StoryPlace', null=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='occupations',
            field=models.ManyToManyField(to='digipal_project.Bonhum_StoryCharacterOccupation', blank=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='religion',
            field=models.ForeignKey(blank=True, to='digipal_project.Bonhum_StoryCharacterReligion', null=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_story_character', through='digipal_project.Bonhum_TextStoryCharacter', to='digipal.Text', blank=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='titles',
            field=models.ManyToManyField(to='digipal_project.Bonhum_StoryCharacterTitle', blank=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='traits',
            field=models.ManyToManyField(to='digipal_project.Bonhum_StoryCharacterTrait', blank=True),
        ),
        migrations.AddField(
            model_name='bonhum_storycharacter',
            name='type',
            field=models.ForeignKey(blank=True, to='digipal_project.Bonhum_StoryCharacterType', null=True),
        ),
        migrations.AddField(
            model_name='bonhum_source',
            name='authors',
            field=models.ManyToManyField(related_name='authors_of_source', through='digipal_project.Bonhum_SourceAuthor', to='digipal.Person', blank=True),
        ),
        migrations.AddField(
            model_name='bonhum_source',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_source', through='digipal_project.Bonhum_TextSource', to='digipal.Text', blank=True),
        ),
        migrations.AddField(
            model_name='bonhum_source',
            name='type',
            field=models.ForeignKey(to='digipal_project.Bonhum_SourceType'),
        ),
        migrations.AddField(
            model_name='bonhum_edition',
            name='work',
            field=models.ForeignKey(to='digipal_project.Bonhum_Work'),
        ),
        migrations.AddField(
            model_name='bonhum_collaborator',
            name='texts',
            field=models.ManyToManyField(related_name='texts_of_collaborator', through='digipal_project.Bonhum_TextCollaborator', to='digipal.Text', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_workcurrentitem',
            unique_together=set([('work', 'current_item')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_work',
            unique_together=set([('title', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_textstorycharacter',
            unique_together=set([('text', 'story_character')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_textsource',
            unique_together=set([('source', 'text')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_textimage',
            unique_together=set([('text', 'image')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_textcollaborator',
            unique_together=set([('text', 'collaborator', 'activity')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_storyplacenamevariant',
            unique_together=set([('name', 'place')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_storyplace',
            unique_together=set([('name', 'parent')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_storycharacternamevariant',
            unique_together=set([('name', 'character')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_sourceauthor',
            unique_together=set([('source', 'author')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_collaborator',
            unique_together=set([('first_name', 'last_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='bonhum_catalogue',
            unique_together=set([('current_item', 'reference')]),
        ),
    ]
