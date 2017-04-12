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
#####DONE!!!
#TODO: must have 2 templates; one for each of the main blog and new post views, your templates extend a base.html template which includes some boilerplate html that will be used on each page, along with some styles to clean up your blogs visuals a bit (see ASCIICHAN excercise)
#####DONE!!!
#TODO: able to submit a new '/newpost' route/view. After submitting a new post your app displays the main blog page. Note that you will likely need to resubmit to view new page
####DONE!!!????
#TODO: if either title or body is left empy in the new post form, the form is rendered again with a helpful error message and any previously entered content in the same form inputs
#####DONE!!!!!



#imports modules

import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db


#sets up jinja2 templates path

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

#contains helper functions
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#defines blogpost entity for db
class blogPost(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    date_created = db.DateTimeProperty(auto_now_add = True)

#sets up index-page, with blog.html template, click title link to add new post
class MainPage(Handler):


    def get(self):
        self.render("blog.html")
#### TODO: IF THEY WANT TO SPLASH INTO A DISPLAY, CHANGE THIS TO :
        #'self.render("blog.html")'
        ##ASK ABOUT THIS!!!!

#sets up blog post input for DB, also sets up error message and retains user input thru the error

class CreateEntry(Handler):
    def render_base(self, title="", body="", error=""):
        self.render("newpost.html", title=title, body=body, error=error)

    def get(self):
        self.render("newpost.html", title="", body="", error="")

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            bp = blogPost(title = title, body = body)
            bp.put()

            self.redirect("/blog/" + str(bp.key().id()))

        else:
            error = "we need both a title and a body!"
            self.render_base(title, body, error)

class blogEntries(Handler):
    def render_blogPosts(self, title="", body="", error=""):
        blogPosts = db.GqlQuery("SELECT * FROM blogPost ORDER BY date_created DESC LIMIT 5")
        self.render("blog.html", title=title, body=body, error=error, blogPosts=blogPosts)

    def get(self):
        self.render_blogPosts()

class viewPostHandler(Handler):
    def render_singlePost(self, id, title="", body="",error=""):
        singlePost = blogPost.get_by_id(int(id), parent=None)
        self.render("singlePost.html", title=title, body=body, error=error, singlePost=singlePost)
    def get(self, id):
        if id:
            self.render_singlePost(id)
        else:
            self.render_singlePost(id, title="no such post!", error="no bost exists with "+ str(id))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', CreateEntry),
    ('/blog', blogEntries),
    webapp2.Route('/blog/<id:\d+>', viewPostHandler)
    ], debug=True)
