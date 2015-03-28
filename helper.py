import urllib
import urllib2

host = "http://localhost:8080"

def perform_request(endpoint):

  request = host + endpoint

  return urllib2.urlopen(request).read()


def create_league(name):

  endpoint = "/createleague?" + urllib.urlencode({"name":name})

  return perform_request(endpoint)
