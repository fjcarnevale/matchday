from google.appengine.ext import ndb

class League(ndb.Model):
  name = ndb.StringProperty()
  teams = ndb.KeyProperty(repeated=True)
  matches = ndb.KeyProperty(repeated=True)

  def add_new_team(self, name):
    team = Team.new_team(name,self)
    team_key = team.put()

    self.teams.append(team_key)
    self.put()
    return team_key

  @classmethod
  def get_leagues(cls):
    return cls.query()

  @staticmethod
  def new_league(name):
    league = League()
    league.populate(name=name)
    league.put()
    return league

class Team(ndb.Model):
  name = ndb.StringProperty()
  league = ndb.KeyProperty()
  matches = ndb.KeyProperty(repeated=True)

  @staticmethod
  def new_team(name, league):
    team = Team()
    team.populate(name = name, league = league.key)
    team.put()
    return team

class Match(ndb.Model):
  date = ndb.DateTimeProperty()
  teams = ndb.KeyProperty(repeated=True)
  league = ndb.KeyProperty()

  @staticmethod
  def new_match(date, teams, league):

    match = Match()
    match.populate(date=date, teams=teams, league=league)
    match.put()

    return match

