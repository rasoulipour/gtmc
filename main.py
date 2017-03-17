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





node = 888
template_dir = os.path.join(os.path.dirname(__file__), 'templates'),
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))



'''
def content_builder():
     content = '<body style="background-color: rgb'+ str(make_rgb())+ '">' + '<p1>' +  str(make_rgb()) + '</p1>'
     return content
'''


class MainPage(Handler):



    def get(self):
        img = "images/abu2.png"

        dictionary = main(img)
        self.render("front.html", dictionary=dictionary, img = img)

    def post(self):
        image = self.request.get("image")
        customUrl = self.request.get("customimage")

        if customUrl != "":
            img = customUrl

        elif image == "one":
            img = "http://www.apogeephoto.com/wp-content/uploads/2016/06/14.jpg"
        elif image == "two":
            img = "https://www.tamilnet.com/img/publish/2009/05/Colombo_Fort_81109_445.jpg"
        elif image == "three":
            img = "https://i.imgur.com/9geCmKm.jpg"


        dictionary = main(img)


        self.render("front.html", dictionary=dictionary, img=img)



app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
