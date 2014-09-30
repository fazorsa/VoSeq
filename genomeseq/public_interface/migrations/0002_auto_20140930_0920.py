# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_interface', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genes',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='genes',
            name='gene_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='genes',
            name='genetic_code',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='genes',
            name='intron',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
