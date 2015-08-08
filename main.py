from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2Decorator
import webapp2
import jinja2
import logging
import os
from apiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache

from googlecalendarconnection import *

__author__ = 'yannick@everspire.com (Yannick Cohen)'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')

MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secret.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS

# http = httplib2.Http(memcache)
service = build('calendar', 'v3')
decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar',
    message=MISSING_CLIENT_SECRETS_MESSAGE)



# decorator = OAuth2Decorator(
#   client_id='494667278516-nlhglp2nq4lm9liftiucbt4sc7rehqo8.apps.googleusercontent.com',
#   client_secret='o55rCc6zRPxoSJgkYO72LAlk',
#   scope='https://www.googleapis.com/auth/calendar',
#   callback_path='/hi')



class MainHandler(webapp.RequestHandler):

  	@decorator.oauth_aware
  	def get(self):
  		variables = {
  			'url': decorator.authorize_url(),
			'has_credentials': decorator.has_credentials()
			}
		template = JINJA_ENVIRONMENT.get_template('grant.html')
		self.response.write(template.render(variables))

  # @decorator.oauth_required
  # def get(self):
  #   # Get the authorized Http object created by the decorator.
  #   http = decorator.http()
  #   # Call the service using the authorized Http object.
  #   request = service.events().list(calendarId='primary')
  #   response = request.execute(http=http)
  #   self.response.write(response)


class AboutHandler(webapp2.RequestHandler):

  @decorator.oauth_required
  def get(self):
    try:
      http = decorator.http()
      # request = service.events().list(calendarId='yannick.d.cohen@gmail.com')
      # response = request.execute(http=http)
      text = 'Hello, %s!' % "Dudeman"


      # print calendarList.list(service, http)
      # print calendarList.listNames(service, http)
      # print events.insert(service, http)

      # calendars.insert(service, http, "Done")
      # calendarList.insert(service, http, 'ek6rosdqsntgg12i1lhbghqu1g@group.calendar.google.com')
      calendars.createDoneCalendar(service, http)

      # text += '<br><br>%s' % response

      template = JINJA_ENVIRONMENT.get_template('welcome.html')
      self.response.write(template.render({'text': text }))
    except client.AccessTokenRefreshError:
      self.redirect('/')


# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
