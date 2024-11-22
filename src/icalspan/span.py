"""
icalspan.span

Get events in an iCalendar between specific dates.
"""

# Imports
from icalendar import Calendar
import requests
from datetime import datetime, date
from dateutil.rrule import rrulestr
import pytz

# ------------------------------------------------------------
#  Read from URL
# ------------------------------------------------------------
def read_from_url(url):
    """
    Read an iCalendar file from a URL.

    Parameters
    ----------
    url : str
        The URL of the iCalendar file.

    Returns
    -------
    str
        The contents of the iCalendar file.
    """
    # Read the iCalendar file
    response = requests.get(url)
    return Calendar.from_ical(response.content)

def untimezone_datetime(dt, tz):
    if type(dt) == date:
        return dt
    if dt.tzinfo is not None:
        dt = dt.astimezone(tz)
        dt = dt.replace(tzinfo=None)
    return dt

def get_events(cal, cal_start_date, cal_end_date, tz = None):
    """
    Get events in an iCalendar between specific dates.

    Parameters
    ----------
    cal : Calendar
        The iCalendar object.
    cal_start_date : date
        The start date.
    cal_end_date : date
        The end date.

    Returns
    -------
    list
        A list of events between the start and end dates.
    """

    # Recurring events may need to reference datetime object. Create a date object to compare with
    cal_start_dt = datetime.combine(cal_start_date, datetime.min.time())
    cal_end_dt = datetime.combine(cal_end_date, datetime.max.time())
    cal_start_d = cal_start_dt.date()
    cal_end_d = cal_end_dt.date()

    # get local timezone if none is specified
    if tz is None:
        tz = datetime.now().astimezone().tzinfo

    events = []
    for event in cal.walk('vevent'):
        # Should we use date or datetime?
        use_datetime = isinstance(event['dtstart'].dt, datetime)

        # Get the event start
        event_start_dt = untimezone_datetime(event['dtstart'].dt,tz)
        if isinstance(event_start_dt, datetime):
            event_start_d = event_start_dt.date()
        else:
            event_start_d = event_start_dt
    
        # Make sure the event has an end date
        if hasattr(event, "dtend"):
            event_end_dt = event['dtend'].dt
        else:
            event_end_dt = event_start_dt
        event_end_dt = untimezone_datetime(event_end_dt,tz)

        # Get the event end date
        if isinstance(event_end_dt, datetime):
            event_end_d = event_end_dt.date()
        else:
            event_end_d = event_end_dt


        rrule = event.get('rrule')
        if rrule is None:
            # Not a recurring event, just check the date
            if event_start_d >= cal_start_date and event_start_d <= cal_end_date:
                events.append(event)

        else: # Recurring event
            start = cal_start_dt
            end = cal_end_dt

            event_start = event_start_dt
            event_end = event_end_dt

            # Remove dt from until attribute
            if "UNTIL" in rrule:
                new_until = rrule['UNTIL'][0]
                if type(new_until) == date:
                    new_until = datetime.combine(new_until, datetime.max.time())
                new_until = untimezone_datetime(new_until, tz)
                new_until = new_until.replace(tzinfo=None)
                rrule['UNTIL'][0] = new_until

            rrule_drr = rrulestr(rrule.to_ical().decode("utf-8"), dtstart=event_start)

            print("xxx" , event)
            print("xxx", rrule)
            print("xxx", rrule_drr)
            print("xxx", start, end)
            print("xxx", event_start)

            for occurrence in rrule_drr.between(start, end):
                print("XXXXXXXX,", occurrence)
        #         if occurrence >= cal_start_date and occurrence <= cal_end_date:
        #             event_copy = event.copy()
        #             event_copy['dtstart'].dt = occurrence
        #             event_copy['dtend'].dt = occurrence
        #             event_copy["rrule"] = None
        #             events.append(event_copy)
    return events