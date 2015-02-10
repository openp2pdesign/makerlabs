# -*- encoding: utf-8 -*-
#
# Access data from techshop.ws
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#

from bs4 import BeautifulSoup
import requests
#Requirement: beautifulsoup4

techshop_url = "http://techshop.ws/locations.html"


class TechShop(object):
    """Represents a TechShop as it is described on techshop.ws."""
    
    def __init__(self):
        self.status = ""
        self.url = ""
        self.name = ""
        self.long = ""
        self.lat = ""
        self.coordinates = ""
        self.province = ""
        self.region = ""
        self.address = ""
        self.city = ""
        self.fablabsio = ""
        self.website = ""
        self.facebook = ""
        self.twitter = ""
        self.email = ""
        self.manager = ""
        self.birthyear = ""
        

def get_labs():
    """Gets data from all labs from techshop.ws."""
    
    r = requests.get(techshop_url)
    soup = BeautifulSoup(r.content)
    
    labs = {}
    
    # Get the labs
    items = soup.find_all("strong")
    for k,i in enumerate(items):
        t = TechShop()
        # Already opened Techshops
        if len(i.contents) == 1:
            t.status = "Open"
            t.name = i.text
            if "http://techshop.ws/" not in i.a['href']:
                t.url = "http://techshop.ws/"+i.a['href']
            else:
                t.url = i.a['href']
        # Under construction Techshops
        elif len(i.contents) == 2:
            t.status = "In planning"
            t.name = i.text
            t.url = ""
        labs[k] = t
    
    for i in labs:
        if labs[i].url != "":
            get_single_lab(labs[i].url)
        exit()
    
    return labs
    
    
def get_single_lab(slug):
    """Gets data from a single lab from techshop.ws."""
    
    r = requests.get(slug)
    soup = BeautifulSoup(r.content)
    print soup.prettify()

    return

    
def labs_count():
    """Gets the number of current Labs registered on makeinitaly.foundation."""
    
    labs = get_labs(data_format="dict")
    
    return len(labs)
    

if __name__ == "__main__":
    # Debug
    #a = data_from_makeinitaly_foundation()
    #print a["query"]["categorymembers"]
    #b = get_lab_dict("WeMake")
    #print b
    get_labs()
    #a = get_fablabs()
    #print a["ouagalab"].name
    #print a["ouagalab"].city
    #b = data_from_fablabs_io()
    #c = fablabs_count()
    #print c
    #print get_fablabs_dict()