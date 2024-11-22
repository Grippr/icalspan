import pytest
from icalendar import Calendar
from datetime import date
from icalspan import span
from datetime import datetime, date

# ------------------------------------------------------------
#   Download an ical file
# ------------------------------------------------------------
def test_span():
    # Test that the function returns a string
    with open ("tests/private/ical_url.txt", "r") as fp:
        ical_url = fp.readline()

    my_cal = span.read_from_url(ical_url)
    assert type(my_cal) == Calendar

    start_date = span.get_events(my_cal, date(2024, 6, 1), date(2024, 8, 31))

# @pytest.fixture
# def sample_calendar():
#     cal = Calendar()
#     event1 = Event()
#     event1.add('summary', 'Event 1')
#     event1.add('dtstart', date(2023, 10, 1))
#     event1.add('dtend', date(2023, 10, 2))
#     cal.add_component(event1)

#     event2 = Event()
#     event2.add('summary', 'Event 2')
#     event2.add('dtstart', date(2023, 10, 5))
#     event2.add('dtend', date(2023, 10, 6))
#     cal.add_component(event2)

#     event3 = Event()
#     event3.add('summary', 'Recurring Event')
#     event3.add('dtstart', date(2023, 10, 1))
#     event3.add('rrule', {'freq': 'daily', 'count': 5})
#     cal.add_component(event3)

#     return cal

# def test_get_events_no_events(sample_calendar):
#     start_date = date(2023, 9, 1)
#     end_date = date(2023, 9, 30)
#     events = span.get_events(sample_calendar, start_date, end_date)
#     assert len(events) == 0

# def test_get_events_single_event(sample_calendar):
#     start_date = date(2023, 10, 1)
#     end_date = date(2023, 10, 1)
#     events = span.get_events(sample_calendar, start_date, end_date)
#     assert len(events) == 1
#     assert events[0]['summary'] == 'Event 1'

# def test_get_events_multiple_events(sample_calendar):
#     start_date = date(2023, 10, 1)
#     end_date = date(2023, 10, 6)
#     events = span.get_events(sample_calendar, start_date, end_date)
#     assert len(events) == 7  # 2 single events + 5 occurrences of the recurring event

# def test_get_events_recurring_event(sample_calendar):
#     start_date = date(2023, 10, 1)
#     end_date = date(2023, 10, 5)
#     events = span.get_events(sample_calendar, start_date, end_date)
#     recurring_events = [event for event in events if event['summary'] == 'Recurring Event']
#     assert len(recurring_events) == 5