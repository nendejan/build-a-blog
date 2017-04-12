#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#TODO: '/blog' route should display 5 most recent posts, to limit the displayed posts in this way you'll need to filter the query results
#TODO: must have 2 templates; one for each of the main blog and new post views, your templates extend a base.html template which includes some boilerplate html that will be used on each page, along with some styles to clean up your blogs visuals a bit (see ASCIICHAN excercise)
#TODO: able to submit a new '/newpost' route/view. After submitting a new post your app displays the main blog page. Note that you will likely need to resubmit to view new page
#TODO: if either title or body is left empy in the new post form, the form is rendered again with a helpful error message and any previously entered content in the same form inputs




import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.ath.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja22.FileSystemLoader(template_dir))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
