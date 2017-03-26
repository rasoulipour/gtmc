from PIL import Image
import operator
import heapq
import urllib, cStringIO
#have to fix the cString  thing so that is is compatible if the host is not a mac



def main(iii):
#var iii is any image link given to us from the front end.

    file = cStringIO.StringIO(urllib.urlopen(iii).read())
    img = Image.open(file)

    def rgb_conv(img):
        rgb_img = img.convert('RGB')
        return rgb_img


    def img_width(img):
        width, height = img.size
        return width

    def img_height(img):
        width, height = img.size
        return height

    def sampler(accuracy = 20): #accuracy mesures how many sample shoul be taken in each dimention
        # accuracy of 20 should be sufficient
        # increading the accuracy dramatically decreses the speed of the the processing due to increase in the data
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
                if sr <= r < (sr+32) and sg <= g < (sg+32) and sb <= b < (sb+32):
                    R += r
                    G += g
                    B += b
                    counter += 1
            avaragecolor += (R//counter),(G//counter),(B//counter)
            Ndic[avaragecolor] = Ndic.pop(i)

        return Ndic



    def colorcube():#making a color cube so we can determin what groups of colors are mor prominant
        cubelist = []
        for i in sampler():
            cube = []
            for e in i:
                e = int(e)
                e = e//32 #i determined that dividing e by 32 will have 8 different numbers for R,G and B which gives us a 512 color palette.
                cube.append(e)

            if cube != [0,0,0] and cube != [1,1,1] and cube != [2,2,2] and cube != [3,3,3] and cube != [4,4,4] and cube != [5,5,5] and cube != [7,7,7]:
                cubelist.append(cube) #excludes the grays

        return cubelist

    def make_rgb(lst):
        rgb_list = []
        for i in lst:
            if i != '[' and i != ']' and i != ',' and i != ' ': #coz I messed up and made the lists into strings
                x = int(i) * 32
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
                    x = int(i) * 32
                    rgb_list.append(x)
            r,g,b = rgb_list
            rgb = r,g,b
            dictionary[rgb] = dictionary.pop(z)

        newA = dict(sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse=True)[:7])
        return newA

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

    return getpure()
