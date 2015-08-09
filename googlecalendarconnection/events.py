import calendarList
import calendars

def insert(service, http):
  event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
      'dateTime': '2015-08-07T10:00:00-04:00',
      'timeZone': 'America/New_York',
    },
    'end': {
      'dateTime': '2015-08-07T13:00:00-04:00',
      'timeZone': 'America/New_York',
    },
    'recurrence': [
      'RRULE:FREQ=DAILY;COUNT=1'
    ],
    'attendees': [
      {'email': 'lpage@example.com'},
      {'email': 'sbrin@example.com'},
    ],
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }

  event = service.events().insert(calendarId='yannick.d.cohen@gmail.com', body=event).execute(http=http)
  # print 'Event created: %s' % (event.get('htmlLink'))
  print event['id']
  return event

def get(service, http, eventId):
  event = service.events().get(calendarId='yannick.d.cohen@gmail.com', eventId=eventId).execute(http=http)

  print event
  return event

def delete(service, http, eventId):
  service.events().delete(calendarId='yannick.d.cohen@gmail.com', eventId=eventId).execute(http=http)

def update(service, http, eventId):
  event = get(service, http, eventId)

  # event['start']['dateTime'] = '2015-08-06T10:00:00-04:00'
  # event['end']['dateTime'] = '2015-08-06T11:00:00-04:00'
  event['status'] = 'confirmed'

  updated_event = service.events().update(calendarId='yannick.d.cohen@gmail.com', eventId=eventId, body=event).execute(http=http)

  print updated_event
  return updated_event

def move(service, http, eventId, fromCalendarId, toCalendarId):
  # toCalendarId = 'ju6fpnhnsed5t2fbof4o5bshj4@group.calendar.google.com'

  updated_event = service.events().move(calendarId=fromCalendarId, eventId=eventId, destination=toCalendarId).execute(http=http)

  print updated_event['summary']
  return updated_event

def moveToDone(service, http, eventId):
  doneCalendar = calendarList.getDoneCalendar(service, http)
  if not doneCalendar:
    doneCalendar = calendars.createDoneCalendar(service, http)
  return move(service, http, eventId, 'yannick.d.cohen@gmail.com', doneCalendar['id'])


