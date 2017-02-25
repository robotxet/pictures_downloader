#!/usr/bin/python
# -*- encoding: utf-8 -*-

import httplib
import magic
import os
import time
import sys
import urllib2

########### Edit From Here ###########

#This list is used to search keywords. You can edit this list to search for google images of your choice.
search_keyword = [
# 'Abaddon',
# 'Alchemist',
# 'Ancient Apparition',
# 'Anti-Mage',
# 'Arc Warden',
# 'Axe',
# 'Bane',
# 'Batrider',
# 'Beastmaster',
# 'Bloodseeker',
# 'Bounty Hunter',
# 'Brewmaster',
# 'Bristleback',
# 'Broodmother',
# 'Centaur Warrunner',
# 'Chaos Knight',
# 'Chen',
# 'Clinkz',
# 'DDClockwerk',
# 'Crystal Maiden',
# 'Dark Seer',
# 'Dazzle',
# 'Death Prophet',
# 'Disruptor',
# 'Doom',
# 'Dragon Knight',
# 'Drow Ranger',
# 'Earth Spirit',
# 'Earthshaker',
# 'Elder Titan',
# 'Ember Spirit',
# 'Enchantress',
# 'Enigma',
# 'Faceless Void',
# 'Gyrocopter',
# 'Huskar',
# 'Invoker',
# 'Io',
# 'Jakiro',
# 'Juggernaut',
# 'Keeper of the Light',
# 'Kunkka',
# 'Legion Commander',
# 'Leshrac',
# 'Lich',
# 'Lifestealer',
# 'Lina',
# 'Lion',
# 'Lone Druid',
# 'Luna',
# 'Lycan',
# 'Magnus',
# 'Medusa',
# 'Meepo',
# 'Mirana',
# 'Morphling',
# 'Monkey King',
# 'Naga Siren',
# 'Nature’s Prophet',
# 'Necrophos',
# 'Night Stalker',
'Nyx Assassin',
'Ogre Magi',
'Omniknight',
'Oracle',
'Outworld Devourer',
'Phantom Assassin',
'Phantom Lancer',
'Phoenix',
'Puck',
'Pudge',
'Pugna',
'Queen of Pain',
'Razor',
'Riki',
'Rubick',
'Sand King',
'Shadow Demon',
'Shadow Fiend',
'Shadow Shaman',
'Silencer',
'Skywrath Mage',
'Slardar',
'Slark',
'Sniper',
'Spectre',
'Spirit Breaker',
'Storm Spirit',
'Sven',
'Techies',
'Templar Assassin',
'Terrorblade',
'Tidehunter',
'Timbersaw',
'Tinker',
'Tiny',
'Treant Protector',
'Troll Warlord',
'Tusk',
'Underlord',
'Undying',
'Ursa',
'Vengeful Spirit',
'Venomancer',
'Viper',
'Visage',
'Warlock',
'Weaver',
'Windranger',
'Winter Wyvern',
'Witch Doctor',
'Wraith King',
'Zeus'
]

prefix = "Dota 2 " # this will be appended before each keyword
#This list is used to further add suffix to your search term. (Example: 'Abaddon high resolution')
keywords = [' high resolution']

images_number = 60

########### End of Editing ###########

#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:
        import urllib.request
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        start_type = s.find('"ity"', start_line+1)
        if start_type == -1:
            img_type = ""
        else:
            end_type = s.find(',"oh"', start_type+1)
            img_type = str(s[start_type+7:end_type-1])
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content, img_type

#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while len(items) < images_number:
        item, end_content, img_type = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append((item, img_type))
            time.sleep(0.1)   #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items


############## Main Program ############

#Download Image Links
i= 0
errorCount=0
while i<len(search_keyword):
    t0 = time.time()   #start the timer
    items = []
    iteration = "Item no.: " + str(i+1) + " -->" + " Item name = " + str(search_keyword[i])
    print (iteration)
    print ("Evaluating...")
    search_keywords = prefix + search_keyword[i]
    search = search_keywords.replace(' ','%20')
    j = 0
    while j<len(keywords):
        pure_keyword = keywords[j].replace(' ','%20')
        url = 'https://www.google.com/search?q=' + search + pure_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html =  (download_page(url))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        j = j + 1
    #print ("Image Links = "+str(items))
    print ("Total Image Links = "+str(len(items)))
    print ("\n")
    i = i+1


    #This allows you to write all the links into a test file.
    # info = open('output.txt', 'a')        #Open the text file called database.txt
    # info.write(str(i) + ': ' + str(search_keyword[i-1]) + ": " + str(items) + "\n\n\n")         #Write the title of the page
    # info.close()                            #Close the file

    t1 = time.time()    #stop the timer
    total_time = t1-t0   #Calculating the total time required to crawl, find and download all the links of 60,000 images
    print("Time taken to parse request: "+str(total_time)+" Seconds")
    print ("Starting Download...")

    # IN this saving process we are just skipping the URL if there is any error

    k=0
    while(k<len(items)):
        from urllib2 import Request,urlopen
        from urllib2 import URLError, HTTPError

        try:
            req = Request(items[k][0], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req)
            DIR = "Pictures"
            if not os.path.exists(DIR):
              os.mkdir(DIR)
            DIR = os.path.join(DIR, "Dota_2")
            if not os.path.exists(DIR):
                os.mkdir(DIR)
            filepath = search_keywords
            filepath = filepath.replace(prefix, "")
            filepath = filepath.split()
            filepath = "_".join(filepath)
            DIR = os.path.join(DIR, filepath)
            if not os.path.exists(DIR):
                os.mkdir(DIR)
            if len(items[k][1]) != 0:
                with open(os.path.join(DIR, str(k+1)+"." + items[k][1]),'wb') as output_file:
                    try:
                        data = response.read()
                        try:
                            type_i = magic.from_buffer(data)
                            print type_i
                            if type_i.find("image", 0, 30):
                                output_file.write(data)
                                print ("saved ====> " + str(k+1)) + " url: " + items[k][0]
                            else:
                                print "wrong data type"
                            response.close();
                        except Exception:
                           print("Probably Magic.from_buffer exception at image "+str(k)) 
                    except Exception:
                           print("Probably httplib.IncompleteRead: IncompleteRead at image "+str(k)) 
            k=k+1;

        except IOError:

            errorCount+=1
            print("IOError on image "+str(k+1))
            k=k+1;

        except HTTPError as e:

            errorCount+=1
            print("HTTPError"+str(k))
            k=k+1;
        except URLError as e:

            errorCount+=1
            print("URLError "+str(k))
            k=k+1;
        except httplib.BadStatusLine:
            errorCount+=1
            print("BadStatusLine "+str(k))
            k=k+1;
print("\n")
print("All are downloaded")
print("\n"+str(errorCount)+" ----> total Errors")

#----End of the main program ----#