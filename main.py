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
    def sort_info(self, json_results):
        voter_info = {}

        voter_info['election_name'] = json_results['election']['name']
        voter_info['day'] = json_results['election']['electionDay']
        line1 = json_results['normalizedInput']['line1']
        city = json_results['normalizedInput']['city']
        state = json_results['normalizedInput']['state']
        zip = json_results['normalizedInput']['zip']
        user_address = "%s, %s, %s %s" % (line1, city, state, zip)
        voter_info['user_address'] = user_address

        location = json_results['pollingLocations'][0]
        voter_info['polling_name'] = location['address']['locationName']
        line1 = location['address']['line1']
        city = location['address']['city']
        state = location['address']['state']
        zip = location['address']['zip']
        hours = location['pollingHours']
        polling_address = '%s, %s, %s %s' % (line1, city, state, zip)
        voter_info['polling_address'] = polling_address

        voter_info['contests'] = json_results['contests']

        return voter_info


    def post(self):
        user_address = self.request.get('address')
        url = "https://www.googleapis.com/civicinfo/v2/voterinfo"
        api_key = 'AIzaSyBTh58yBdRemPRhsEsJ4PipEGKqdHUY_XA'

        payload = {'address': user_address, 'key': api_key}
        res = requests.get(url, params=payload) #json results about the voters infopage
        json_res = json.loads(res.text)

        json_res = self.sort_info(json_res)

        res_dict = {'results': json_res}

        info_template = jinja_current_directory.get_template('templates/infopage.html')
        self.response.write(info_template.render(res_dict))

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/info', InfoPage)
], debug=True)
