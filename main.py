import webapp2
import os
import jinja2
import ast
from google.appengine.api import urlfetch
import requests
import requests_toolbelt.adapters.appengine
import json

# Use the App Engine Requests adapter. This makes sure that Requests uses URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

jinja_current_directory = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

app = webapp2.WSGIApplication([
    ('/', HomePage)
], debug=True)
