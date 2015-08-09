### Return all information about each Google Calendar
def list(service, http):
	page_token = None
	calendar_list_items = []
	while True:
		calendar_list = service.calendarList().list(pageToken=page_token).execute(http=http)
		for calendar_list_entry in calendar_list['items']:
			calendar_list_items.append(calendar_list_entry)
			page_token = calendar_list.get('nextPageToken')
		if not page_token:
			break
	return calendar_list_items

### Return a list of the Google Calendar names
def listNames(service, http):
	calendar_list = list(service, http)
	calendar_list_names = []
	for calendar_list_entry in calendar_list:
		calendar_list_names.append(calendar_list_entry['summary'])
	return calendar_list_names

### Create a new calendar
def insert(service, http, calendarId):

	calendar_list_entry = {
		'id': calendarId,
		# 'colorId': "15"
		'backgroundColor': '#9fc6e7',
		'foregroundColor': '#000000',
		'selected': True
	}

	created_calendar_list_entry = service.calendarList().insert(body=calendar_list_entry, colorRgbFormat=True).execute(http=http)
	return created_calendar_list_entry['summary']

def getDoneCalendar(service, http):
	calendar_list = list(service, http)
	for calendar in calendar_list:
		if calendar['summary'].lower() == "done":
			return calendar