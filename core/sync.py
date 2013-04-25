from datetime import datetime
import os, re
import feedparser
from core.models import Pasty


def sync_rss_source(source):
    if not source.parser() in globals():
        print('parser %s not found for' % source.parser())
        return
    print('feeding data from ' + source.title)
    try:
        data = feedparser.parse(source.sync_url)
        sync_date = to_date(data.feed.updated_parsed)
        if source.sync_date and source.sync_date >= sync_date:
            print('source is already up to date')
            return
        for entry in data.entries:
            pastry = globals()[source.parser()](sync_date, source, entry)
            # Save only if pastry is newer than previous sync date
            if pastry and (not source.sync_date or pastry.date > source.sync_date):
                pastry.save()
                print('saved pastry %s' % pastry)
        source.sync_date = sync_date
        source.save()
        print('successful sync for date %s' % sync_date)
    except Exception as e:
        print('sync failed: %s' % e)


# TODO: how should I parse perashki.ru?!

def strip(text):
    strip_pattern = re.compile('</?p>|</?div>')
    br_pattern = re.compile('<br ?/?>')
    space_pattern = re.compile('\s\s+')
    text = strip_pattern.sub('', text)
    text = space_pattern.sub(' ', text)
    text = br_pattern.sub(os.linesep, text)
    return text

def to_date(feed_date):
    if not feed_date:
        return None
    return datetime(feed_date[0], feed_date[1], feed_date[2], feed_date[3], feed_date[4], feed_date[5])


def pirozhki_ru_livejournal_com(sync_date, source, entry):
    p = Pasty()
    p.text = strip(entry['summary_detail']['value'])
    p.date = to_date(entry['published_parsed'])
    if not p.date: p.date = sync_date
    p.source = source.url
    if len(p.text) > 255:
        return None
    return p


def stishkipirozhki_ru(sync_date, source, entry):
    p = Pasty()
    p.text = strip(entry['content'][0]['value'])
    p.date = to_date(entry['published_parsed'])
    if not p.date: p.date = sync_date
    p.source = source.url
    return p
