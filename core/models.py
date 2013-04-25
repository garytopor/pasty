# -*- coding: utf-8 -*-

import os
import re
from urlparse import urlparse
from django.db import models


class Pasty(models.Model):
    text = models.TextField(u'Текст пирожка')
    date = models.DateTimeField(u'Дата публикации', blank=True, null=True)
    source = models.URLField(u'Источник', blank=True)
    votes = models.IntegerField(u'Голосов', default=0, null=True)
    source_pattern = re.compile(r'''http://(?:www\.)?(.+)''')

    def short_text(self):
        return self.text[:37].replace(os.linesep, ' \ ') + '...'

    def source_title(self):
        return urlparse(self.source).hostname

    def __unicode__(self):
        return self.short_text()

    @staticmethod
    def rnd():
        if Pasty.objects.count() == 0:
            return None
        return Pasty.objects.order_by('?')[0]


class Source(models.Model):
    title = models.TextField(u'Название источника')
    url = models.URLField(u'Ссылка')
    sync_url = models.URLField(u'URL синхронизации', blank=True)
    sync_date = models.DateTimeField(u'Дата последней синхронизации', blank=True, null=True)
    parser_pattern = re.compile('[.-]')

    def __unicode__(self):
        return self.title

    def parser(self):
        return self.parser_pattern.sub('_', self.title)
