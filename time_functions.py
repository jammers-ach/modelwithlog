import datetime
from django.utils.safestring import mark_safe


class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)

def endStartWeek(startDate=datetime.datetime.now()):
    if(type(startDate) == datetime.datetime):
        today = datetime.datetime.date(startDate)
    else:
        today = startDate
    startWeek = today - datetime.timedelta(today.isoweekday()-1) 
    endWeek = today + datetime.timedelta(8-today.isoweekday())
    return (startWeek,endWeek)

def html_display(paragraph):
    if paragraph != None:
        return mark_safe(paragraph.replace('\n','<br/>'))
    else:
        return ""
    
def getLastAndNextMonth(dateInMonth=datetime.date.today()):
    """Gives you two dates in the last month and this month"""
    d1 = get_first_day(dateInMonth,d_months=1)
    d2 = get_first_day(dateInMonth,d_months=-1)
    return (d2,d1)
    
def daysInMonthWithBoundry(dateInMonth=datetime.date.today()):
    """Gives you a nice iterable list of months, but with a few days boundry either side so it fits into a nice 7 column display"""
    start_month,end_month = endStartMonth(dateInMonth)
    
    extra_start = start_month - datetime.timedelta(start_month.isoweekday()- 1) 
    extra_end = end_month - datetime.timedelta(end_month.isoweekday()) + datetime.timedelta(7)
    
    timeDiff = (extra_end-extra_start)
    return [ extra_start + datetime.timedelta(days=x) for x in range(0,timeDiff.days+1) ]

def daysInWeek(dayInWeek):
    """Gives you all the dates in a week Monday-Sunday"""
    
    start = dayInWeek -  datetime.timedelta(dayInWeek.weekday())

    return [start + datetime.timedelta(days=x) for x in range(0,7)]

def daysInWeek2(dayInWeek):
    """Gives you all the dates in a 2 week period from the monday before you started to
    the sunday afterward"""
    
    start = dayInWeek -  datetime.timedelta(dayInWeek.weekday())

    return [start + datetime.timedelta(days=x) for x in range(0,14)]

def daysInMonth(dateInMonth=datetime.date.today()):
    """Gives you an iterable list for all the days in this month""" 
    if(type(dateInMonth) == datetime.datetime):
        today = datetime.datetime.date(dateInMonth)
    else:
        today = dateInMonth
        
    #Find out how many days we have in the month
    start,end = endStartMonth(today)
    timeDiff = (end-start)

    #Return that list
    return [ start + datetime.timedelta(days=x) for x in range(0,timeDiff.days+1) ]
    

    
def endStartMonth(dateInMonth=datetime.date.today()):
    if(type(dateInMonth) == datetime.datetime):
        today = datetime.datetime.date(dateInMonth)
    else:
        today = dateInMonth
    
    return (get_first_day(today),get_last_day(today))
    


def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m-1, 12)
    return datetime.date(y+a, m+1, 1)

def get_last_day(dt):
    return get_first_day(dt, 0, 1) + datetime.timedelta(-1)


def days_between(start,end):
    days = []
    while(start != end):
        days.append(start)
        start = start + datetime.timedelta(1) 
        
    return days

def days_after(start,number):
    days = []
    for i in range(number):
        days.append(start + datetime.timedelta(i))
    return days
    


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    
    http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    """
    from datetime import datetime
    from django.utils import timezone
    now = timezone.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        print 'now:',now,'time:',time
        diff = now - time 
    elif not time:
        diff = now - now
    else:
        raise Exception('Time is in unknown format %s' % type(time))
        
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"


def pretty_date_short(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    
    http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    else:
        try:
            diff = now - time
        except:
            return '' 

        
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0 or second_diff < 0:
        now = datetime.now()
        if type(time) is int:
            diff = datetime.fromtimestamp(time) - now
        elif isinstance(time,datetime):
            diff = time - now  
        second_diff = diff.seconds
        day_diff = diff.days

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + "s"
        if second_diff < 3600:
            return str( second_diff / 60 ) + "m"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + "h"

    if day_diff < 7:
        return str(day_diff) + "d " + str( second_diff / 3600 ) + "h"
    
    if day_diff < 365:
        return str(day_diff/7) + "w " + str( day_diff - (int(day_diff/7)*7)) + "d"

    return str(day_diff/365) + "y"


def delta_t_as_time_left(delta_t):
    s = (delta_t.days*24*60*60) + delta_t.seconds
    if (s < 0):
        s = -s
    return seconds_to_time_left_string(s)

#http://stackoverflow.com/questions/538666/python-format-timedelta-to-string
def seconds_to_time_left_string(total_seconds):
    s = int(total_seconds)

    years = s // 31104000
    if years > 1:
        return '%d years' % years
    s = s - (years * 31104000)
    months = s // 2592000
    if years == 1:
        r = '1 year'
        if months > 0:
            r += ' and %d months' % months
        return r
    if months > 1:
        return '%d months' % months
    s = s - (months * 2592000)
    days = s // 86400
    if months == 1:
        r = '1 month'
        if days > 0:
            r += ' and %d days' % days
        return r
    if days > 1:
        return '%d days' % days
    s = s - (days * 86400)
    hours = s // 3600
    if days == 1:
        r = '1 day'
        if hours > 0:
            r += ' and %d hours' % hours
        return r 
    s = s - (hours * 3600)
    minutes = s // 60
    seconds = s - (minutes * 60)
    if hours >= 6:
        return '%d hours' % hours
    if hours >= 1:
        r = '%d hours' % hours
        if hours == 1:
            r = '1 hour'
        if minutes > 0:
            r += ' and %d minutes' % minutes
        return r
    if minutes == 1:
        
        if seconds > 30:
            r = 'about 1 minutes'
        else:
            r = '1 minute'
        return r
    if minutes == 0:
        return 'under a minute'
    if seconds == 0:
        return '%d minutes' % minutes
    return '%d minutes' % (minutes)
