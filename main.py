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
from PIL import Image
from sys import argv
import operator

img = Image.open("image1.jpg") #this is a specific image that I tested the code on

def rgb_conv(img):
    rgb_img = img.convert('RGB')
    return rgb_img


def img_width(img):
    width, height = img.size
    return width

def img_height(img):
    width, height = img.size
    return height

def sampler(accuracy = 30): #accuracy mesures how many sample shoul be taken in each dimention
    # accuracy of 20 should be sufficient
    pixel_list = []  #an empty list that would store all the data from different pixels in it
    w = img_width(img)
    h = img_height(img)
    x = 0
    y = 0
    for poo in range(0, h, h//accuracy): #i did this so the image is divided into equal sections for sampling
        for goo in range(0, w, w//accuracy):

            rgb_img = rgb_conv(img)
            r, g, b = rgb_img.getpixel((goo, y))

            thiscolorcode = [r,g,b]
            #print(thiscolorcode)  #activate this if you want to see the samples
            pixel_list.append(thiscolorcode)
        y = poo
    #print(len(pixel_list)) #prints the number of samples it takes
    return pixel_list



'''
def image_is_complex():

    #this function determines whether
    #the image is a photo or an illustraited
    #image with less colors in composition

    if len(cubecounter()) > 30:
        return True
    else:
        return False


def size_of_colorcube():


    #this function returns a number
    #that would go into color cube function
    #and determines the size of the color cube
    #based on what kind of image is being analyzed
    #the more realistic the image aka the more colors
    #the higher the number that this function returns
    #the higher the number it returns the shorter the
    #dictionary and wider its units.


    if image_is_complex()==True:
        return 32
    else:
        return 16

'''


def colorcube():
    cubelist = []
    for i in sampler():
        cube = []
        for e in i:
            e = int(e)
            e = e//32
            cube.append(e)
        cubelist.append(cube)

    return cubelist



def cubecounter():
    dictionary = {}
    accurance_list = []
    cblist_str = [str(item) for item in colorcube()]

    for i in cblist_str:
        a = cblist_str.count(i)
        dictionary[i] = a
        accurance_list += [a]

    accurance_list = sorted(accurance_list)

    return dictionary, accurance_list



def analyze():
    dictionary, accurance_list = cubecounter()
    print (dictionary)
    print('i found roughly', len(dictionary), 'colors, in which', max(dictionary, key=dictionary.get), 'is the most prominant' )


    #for pix in dictionary:
    #    print(pix, dictionary[pix])






analyze()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
