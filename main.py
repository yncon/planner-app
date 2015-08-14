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

service = build('calendar', 'v3')
decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar',
    message=MISSING_CLIENT_SECRETS_MESSAGE)


template_directory = os.path.join(os.path.dirname(__file__), 'app')
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_directory),
                                       autoescape = True)

class Helper(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class ActionsHandler(Helper):
    def get(self):
        self.render('actions.html')


class MainHandler(Helper):

    @decorator.oauth_aware
    def get(self):
        variables = {
            'url': decorator.authorize_url(),
            'has_credentials': decorator.has_credentials()
            }
        # template = JINJA_ENVIRONMENT.get_template('grant.html')
        # self.response.write(template.render(variables))
        self.render('index.html')


class AboutHandler(webapp2.RequestHandler):

  @decorator.oauth_required
  def get(self):
    try:
      http = decorator.http()

      # request = service.events().list(calendarId='yannick.d.cohen@gmail.com')
      # response = request.execute(http=http)
      # text = '<br><br>%s' % response

      text = 'Hello, %s!' % "Dudeman"


      # print calendarList.list(service, http)
      # print calendarList.listNames(service, http)
      # print events.insert(service, http)

      # calendars.insert(service, http, "Done")
      # calendarList.insert(service, http, 'ek6rosdqsntgg12i1lhbghqu1g@group.calendar.google.com')
      # calendars.createDoneCalendar(service, http)

      event = events.insert(service, http)
      print event
      print event['id']
      # events.delete(service, http, eventId)
      
      # eventId = "fhgfsserke56huame8fr3bcgbs"
      # events.get(service, http, eventId)
      # events.update(service, http, eventId)
      # events.move(service, http, eventId, "yannick.d.cohen@gmail.com", "Done")
      print events.moveToDone(service, http, event['id'])
      

      template = JINJA_ENVIRONMENT.get_template('welcome.html')
      self.response.write(template.render({'text': text }))
    except client.AccessTokenRefreshError:
      self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
