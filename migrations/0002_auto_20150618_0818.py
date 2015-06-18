# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelwithlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelstamp',
            name='user_objid',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
