# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digipal_project', '0003_auto_20210504_1026'),
        ('digipal_text', '0003_textcontent_attribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='textcontent',
            name='edition',
            field=models.ForeignKey(related_name='text_contents', to='digipal_project.Bonhum_Edition', null=True),
        ),
        migrations.AlterField(
            model_name='textcontent',
            name='item_part',
            field=models.ForeignKey(related_name='text_contents', to='digipal.ItemPart', null=True),
        ),
        migrations.AlterField(
            model_name='textcontent',
            name='text',
            field=models.ForeignKey(related_name='text_contents', to='digipal.Text', null=True),
        ),
    ]
