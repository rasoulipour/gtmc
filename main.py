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
import webapp2
import os
from algo import main
import jinja2
import datetime
from google.appengine.ext import db
import ast
import operator



template_dir = os.path.join(os.path.dirname(__file__), 'templates'),
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)



class CC(db.Model):
    tag = db.StringProperty(required = True)
    colorcode = db.StringProperty(required = True)
    dominant = db.StringProperty(required = True)
    totalpx = db.IntegerProperty(required = True)
    confidence = db.FloatProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):

    def get(self):
        img = "images/abu2.png images/abu2.png images/abu2.png images/abu2.png images/abu2.png images/abu2.png images/abu2.png images/abu2.png images/abu2.png"
        default_tag = "COLOR OF THE DAY"

        dictionary, totalpx, dominant = main(img)

        q = db.GqlQuery('SELECT * FROM CC ORDER BY created DESC LIMIT 5')

        queryDict = {}
        for n in range(5):
            queryDict[n] = ast.literal_eval(q[n].colorcode)

        self.render("front.html", dictionary=dictionary, totalpx = totalpx, q = q, tag=default_tag, queryDict = queryDict)





    def post(self):
        urlLinks = self.request.get("urllink")
        tag = self.request.get("tag")
        img = urlLinks

        dictionary, totalpx, dominant = main(img)

        data_input = CC(tag= tag, colorcode= str(dictionary), dominant = str(dominant), totalpx = totalpx, confidence = 50.0)
        data_input.put()

        q = db.GqlQuery('SELECT * FROM CC ORDER BY created DESC LIMIT 5')

        queryDict = {}
        for n in range(5):
            queryDict[n] = ast.literal_eval(q[n].colorcode)

        self.render("front.html", dictionary=dictionary, totalpx=totalpx, tag = tag, q=q, queryDict = queryDict)

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
