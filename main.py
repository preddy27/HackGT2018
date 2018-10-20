import webapp2
import os
import os.path
import jinja2
# import ast
# from google.appengine.api import urlfetch
import requests
import requests_toolbelt.adapters.appengine
import json

# Use the App Engine Requests adapter. This makes sure that Requests uses URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

jinja_current_directory = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

class HomePage(webapp2.RequestHandler):
    def get(self):
        # render the main page
        main_template = jinja_current_directory.get_template('templates/mainpage.html')
        self.response.write(main_template.render())

class InfoPage(webapp2.RequestHandler):
    def post(self):
        user_address = self.request.get('address')
        url = "https://www.googleapis.com/civicinfo/v2/voterinfo"
        api_key = 'AIzaSyBTh58yBdRemPRhsEsJ4PipEGKqdHUY_XA'
        payload = {'address': user_address, 'key': api_key}
        res = requests.get(url, params=payload) #json results about the voters infopage
        json_res = json.loads(res.text)

        test = {'results': json_res}

        info_template = jinja_current_directory.get_template('templates/infopage.html')
        self.response.write(info_template.render(test))

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/info', InfoPage)
], debug=True)
