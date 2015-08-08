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
  print 'Event created: %s' % (event.get('htmlLink'))