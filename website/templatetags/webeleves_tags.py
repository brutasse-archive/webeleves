from django import template
import datetime

register = template.Library()


MINUTE = 60
HOUR = 60 * 60
DAY = 60 * 60 * 24
WEEK = 60 * 60 * 24 * 7
MONTH = 60 * 60 * 24 * 30


@register.filter(name='ago')
def ago(value):
    delta = datetime.datetime.utcnow() - value
    offset = delta.seconds + delta.days * DAY
    plural = ''
    value = offset // MONTH
    unit = 'mois'
    if offset < MONTH:
        value = offset // WEEK
        unit = 'semaine'
        plural = 's'
    if offset < WEEK:
        value = offset // DAY
        unit = 'jour'
        plural = 's'
    if offset < DAY:
        value = offset // HOUR
        unit = 'heure'
        plural = 's'
    if offset < HOUR:
        value = offset // MINUTE
        unit = 'minute'
        plural = 's'
    if offset < MINUTE:
        value = offset
        unit = 'seconde'
        plural = 's'
    if value == 1:
        plural = ''
    return 'il y a %s %s%s' % (value, unit, plural)

