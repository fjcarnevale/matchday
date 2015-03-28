import webapp2
import jinja2
import os

from webapp2_extras import sessions
from google.appengine.ext import ndb
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

class CreateTeam(BaseHandler):
  def get(self):
    league_key = ndb.Key(urlsafe = self.request.get("league_key"))
    league = league_key.get()

    league.add_new_team(self.request.get("team_name"))

    self.redirect("/leagueinfo?league_key="+self.request.get("league_key"))
  
class LeagueInfo(BaseHandler):
  def get(self):
    league_key = ndb.Key(urlsafe = self.request.get("league_key"))
    league = league_key.get()

    teams = [team_key.get() for team_key in league.teams]

    template = JINJA_ENVIRONMENT.get_template('leagueinfo.html')
    self.response.write(template.render({"league":league,"teams":teams}))


# Path mappings
application = webapp2.WSGIApplication([
  ('/', Index),
  ('/createleague', CreateLeague),
  ('/createteam'  , CreateTeam),
  ('/leagueinfo'  , LeagueInfo)
], config=config, debug=True)















