import webapp2
import jinja2
import os

from webapp2_extras import sessions

from models import League

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# Sourced from https://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
class BaseHandler(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
      # Returns a session using the default cookie key.
      return self.session_store.get_session()

class Index(BaseHandler):
  """ Handles requests to the main page """
  def get(self):
    leagues = League.get_leagues()

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render({"leagues":leagues}))

class CreateLeague(BaseHandler):
  def get(self):
    league = League.new_league(self.request.get("name"))

    self.response.write("Created league %s" % league.name)

    leagues = League.get_leagues()

    for l in leagues:
      print l

# Path mappings
application = webapp2.WSGIApplication([
  ('/', Index),
  ('/createleague', CreateLeague)
], config=config, debug=True)















