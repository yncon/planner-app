import calendarList

def insert(service, http, calendarSummary):
	calendar = {
		'summary': calendarSummary,
		'timeZone': 'America/New_York',
	}

	created_calendar = service.calendars().insert(body=calendar).execute(http=http)
	calendarList.insert(service, http, created_calendar['id'])

	print created_calendar['id']
	return created_calendar

def createDoneCalendar(service, http):
	return insert(service, http, "Done")
