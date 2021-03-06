#image analysis algorithm by Mohammad Rasoulipour 2017 for SEBCA

from PIL import Image
import operator
import heapq
import urllib
import requests
from google.appengine.api import urlfetch

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO



#have to fix the cString  thing so that is  compatible if the host is not a mac - fixed

urlfetch.set_default_fetch_deadline(5)

def main(raw_urls, displaygray):
#var raw_urls is a string cluster of image urls that are sent from the front end - gotten from the value tag of url

    raw_urls = raw_urls.split() #makes the string into a list based on the spaces


    # Below: mechanism to identify the addresses that are given are URLs or Local Addresses
    URL = False
    firstAddress = raw_urls[0] # firstAddress is the first address given in the list 'raw_urls'
    firstChar = firstAddress[0] # firstAddress is the first character in the first address

    if firstChar == "h" or firstChar == "H":
        URL = True


    if URL:

        links_dict={}  # a dictionary that will contain all the links with certain variables
        for x in range(9):
            try:
                links_dict["link{0}".format(x)] = StringIO(urlfetch.fetch(raw_urls[x]).content)
            except:
                links_dict["link{0}".format(x)] = "images/blank.png"


        list_im = [links_dict["link0"],links_dict["link1"],links_dict["link2"],links_dict["link3"],links_dict["link4"],links_dict["link5"],links_dict["link6"],links_dict["link7"],links_dict["link8"]]


    else:
        list_im = raw_urls



    #images = map(Image.open, list_im)


    new_im = Image.new('RGB', (300,300))
    total_width = 300
    max_height = 300
    x_offset = 0
    y_offset = 0

    for im in list_im:
        try:
            i = Image.open(im)
        except:
            i = Image.open("images/blank.png")

        images = (i.thumbnail((100,100), Image.NEAREST), list_im)
        new_im.paste(i, (x_offset,y_offset))
        x_offset += 100
        print(x_offset)
        if x_offset == 300:
            x_offset = 0
            y_offset += 100
            print(y_offset)

    '''
    for u in images:
        images = (u.thumbnail((100,100), Image.NEAREST), images)
        new_im.paste(u, (x_offset,y_offset))
        x_offset += 100
        print(x_offset)
        if x_offset == 300:
            x_offset = 0
            y_offset += 100
            print(y_offset)
    '''
    #widths, heights = zip(*(i.size for i in images))
    #new_im.save('images/test.jpg')

    img = new_im



################################################### analyzing the image ######################################

    def sampler(): #accuracy mesures how many sample should be taken in each dimention
        # accuracy of 20 should be sufficient
        # increading the accuracy dramatically decreses the speed of the the processing due to increase in the data
        pixel_list = []  #an empty list that would store all the data from different pixels in it
        w = 300
        h = 300
        x = 0
        y = 0
        #divider = -5 #this is a variale that will be squared and determine how much the sampler jumps.
        #selector = 0 #since we have 3 images on each side we want to repeat the process three times

        background_sampler =[]

        sectionlist = [1,25,41,50,54,55,56,60,69,85,98,
        101,125,141,150,154,155,156,160,169,185,198,
        201,225,241,250,254,255,256,260,269,285,298] #an X^2 equasion that x gets numbers between [-5-5] and describes how many steps a sampler should jump

        for row in sectionlist: #i did this so the image is divided into sections for sampling
            for column in sectionlist:
                r, g, b = img.getpixel((column, y))



                thiscolorcode = [r,g,b]
                #print(thiscolorcode)  #activate this if you want to see the samples
                if thiscolorcode != [0,0,0] and thiscolorcode != [100,100,100]:
                    pixel_list.append(thiscolorcode)
            y = row
        #print(len(pixel_list)) #prints the number of samples it takes
        return pixel_list

    def getpure():#goes back and checks the avarage of the dominant colors
        dictionary = cubecounter()
        Ndic = cubecounter()
        for i in dictionary: #gives me a few of the dominant colors
            sr,sg,sb = i  #sr: siplified red
            avaragecolor = ()
            R,G,B = 0,0,0
            counter = 0
            for z in sampler():
                r,g,b = z
                if sr <= r < (sr+64) and sg <= g < (sg+64) and sb <= b < (sb+64):
                    R += r
                    G += g
                    B += b
                    counter += 1
            avaragecolor += (R//counter),(G//counter),(B//counter)
            Ndic[avaragecolor] = Ndic.pop(i)

        #Ndic = sorted(Ndic.iteritems(), key=operator.itemgetter(1)) #sorts but give back a list instead of a dict! so no good!

        return Ndic



    def colorcube():#making a color cube so we can determin what groups of colors are mor prominant
        cubelist = []

        for i in sampler():
            cube = []
            for e in i:
                e = int(e)
                e = e//64 #i determined that dividing e by 32 will have 8 different numbers for R,G and B which gives us a 512 color palette.
                cube.append(e)


            if displaygray == "checked":
                cubelist.append(cube)


            else:#excludes the grays
                if cube != [0,0,0] and cube != [1,1,1] and cube != [2,2,2] and cube != [3,3,3] and cube != [4,4,4] and cube != [5,5,5] and cube != [7,7,7]:
                    cubelist.append(cube)


        return cubelist

    def make_rgb(lst):
        rgb_list = []
        for i in lst:
            if i != '[' and i != ']' and i != ',' and i != ' ': #coz I messed up and made the lists into strings
                x = int(i) * 64
                rgb_list.append(x)
        [r,g,b] = rgb_list
        return r, g, b

    def cubecounter():
        dictionary = {}
        cblist_str = [str(item) for item in colorcube()]

        for z in cblist_str:
            a = cblist_str.count(z)
            dictionary[z] = a
            rgb_list=[]
            for i in z: #tomake them back into tuples so the rgb is read easier
                if i != '[' and i != ']' and i != ',' and i != ' ': #coz I messed up and made the lists into strings
                    x = int(i) * 64
                    rgb_list.append(x)
            r,g,b = rgb_list
            rgb = r,g,b
            dictionary[rgb] = dictionary.pop(z)

        newA = dict(sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
        return newA


    def totalpx(): #this function gives the totla number of samples from the major colors (for front end use)
        newA = cubecounter()
        counter = 0
        for i in newA:
            counter += int(newA[i])
        return counter

    def getNumberOfColors():
        return len(cubecounter())

    def getDominant():
        dictionary = cubecounter()
        return max(dictionary, key=dictionary.get)
        #return ( dictionary ,'i found roughly', len(dictionary), 'colors, in which', max(dictionary, key=dictionary.get), 'is the most prominant' )

    def sortcolor():
        dictionary = cubecounter()
        sums = 0
        for key, value in sorted(dictionary.iteritems(), key=lambda (k,v): (v,k)):
            sums += value
        return sums

    return getpure(), totalpx(), getDominant(), displaygray


#################################################### tests #############################################
#lnk= "http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg http://zns.india.com/upload/2012/6/15/david-beckham150.jpg "

#img = [lnk,lnk,lnk,lnk,lnk,lnk,lnk,lnk,lnk]
#img = str(img)
#img = [x.strip() for x in img.split('\"')]
'''
#tup = ("images/abu2.png","images/banner.png","images/abu2.png","images/abu2.png","images/abu2.png","images/abu2.png","images/abu2.png","images/abu2.png","images/abu2.png")
a, b = main(lnk)
print(type(a))
'''
