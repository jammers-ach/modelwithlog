from django import template
from modelwithlog.time_functions import pretty_date, pretty_date_short
import datetime


register = template.Library()

@register.filter
def ago(value):
    return pretty_date(value)



@register.filter
def ago_short(value):
    return pretty_date_short(value)

@register.filter
def month_lookup(value):
    return datetime.date(2014,value,1)

@register.filter
def hours(value):
    '''Turns minutes into hours and minutes'''
    h = int(value/60)
    m = value%60
    return '%dh %dm' % (h,m) 
