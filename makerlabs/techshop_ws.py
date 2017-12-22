# -*- encoding: utf-8 -*-
#
# Access data from techshop.ws
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab

import json
from bs4 import BeautifulSoup
import requests
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim
import pandas as pd


# Geocoding variable
geolocator = Nominatim()

# Endpoints
techshop_us_url = "http://techshop.ws/locations.html"
techshop_global_url = "http://techshop.ws/ts_global.html"


class Techshop(Lab):
    """Represents a Techshop as it is described on techshop.ws."""

    def __init__(self):
        self.source = "techshop.ws"
        self.lab_type = "Techshop"


def data_from_techshop_ws(tws_url):
    """Scrapes data from techshop.ws."""

    r = requests.get(tws_url)
    if r.status_code == 200:
        data = BeautifulSoup(r.text, "lxml")
    else:
        data = "There was an error while accessing data on techshop.ws."

    return data


def get_labs(format):
    """Gets Techshop data from techshop.ws."""

    techshops_soup = data_from_techshop_ws(techshop_us_url)
    techshops = {}

    # Load all the TechShops
    # By first parsing the html

    data = techshops_soup.findAll('div', attrs={'id': 'main-content'})
    for element in data:
        links = element.findAll('a')
        hrefs = {}
        for k, a in enumerate(links):
            if "contact" not in a['href']:
                hrefs[k] = a['href']
        for k, v in hrefs.iteritems():
            if "http://techshop.ws/" not in v:
                hrefs[k] = "http://techshop.ws/" + v
            else:
                hrefs[k] = v
        for k, v in hrefs.iteritems():
            if "http://techshop.com/" in v:
                hrefs[k] = v.replace("http://techshop.com/", "")

    # Remove duplicate pages
    hr = []
    for key, value in hrefs.iteritems():
        if value not in hr:
            hr.append(value)
    hrefs = hr

    # Check all pages
    for page in hrefs:
        data = data_from_techshop_ws(page)
        current_lab = Techshop()
        name = data.title.contents[0].split('-- ')[1].encode('utf-8')
        if "TechShop" not in name:
            name = "TechShop " + name
        current_lab.name = name
        current_lab.slug = name
        current_lab.url = page
        # Find Facebook and Twitter links
        current_lab.links = {"facebook": "", "twitter": ""}
        page_links = data.findAll('a')
        for link in page_links:
            if link.has_attr("href"):
                if "facebook" in link.attrs["href"]:
                    current_lab.links["facebook"] = link.attrs["href"]
                if "twitter" in link.attrs["href"]:
                    current_lab.links["twitter"] = link.attrs["href"]
        # Find the coordinates by analysing the embedded google map
        iframes = data.findAll('iframe')
        if len(iframes) != 0:
            for iframe in iframes:
                embed_url = iframe.attrs["src"]
                if "google" in embed_url:
                    two_d = embed_url.find("2d")
                    three_d = embed_url.find("3d")
                    longitude = embed_url[two_d:].split('!')[0]
                    latitude = embed_url[three_d:].split('!')[0]
                    longitude = longitude[2:]
                    latitude = latitude[2:]
        # ... or the link to google map
        else:
            page_links = data.findAll('a')
            for link in page_links:
                # one case...
                if "maps.google.com/" in link.attrs["href"]:
                    embed_url = link.attrs["href"]
                    if "ll=" in embed_url:
                        first_string = embed_url.split('&sspn')[0]
                        coordinates = first_string.split('ll=')[1]
                        latitude = coordinates.split(',')[0]
                        longitude = coordinates.split(',')[1]
                # ... another case
                elif "www.google.com/maps" in link.attrs["href"]:
                    embed_url = link.attrs["href"]
                    if "1d" in embed_url:
                        one_d = embed_url.find("1d")
                        two_d = embed_url.find("2d")
                        longitude = embed_url[one_d:].split('!')[0]
                        latitude = embed_url[two_d:].split('!')[0]
                        longitude = longitude[2:]
                        latitude = latitude[2:]
        current_lab.latitude = latitude
        current_lab.longitude = longitude
        current_lab.continent = "North America"
        current_lab.country_code = "USA"
        current_lab.country = "United States of America"
        location = geolocator.reverse((latitude, longitude))
        if "city" in location.raw["address"]:
            current_lab.county = location.raw["address"]["city"].encode(
                'utf-8')
        if "county" in location.raw["address"]:
            current_lab.county = location.raw["address"]["county"].encode(
                'utf-8')
        if "state" in location.raw["address"]:
            current_lab.state = location.raw["address"]["state"].encode(
                'utf-8')
        if "postcode" in location.raw["address"]:
            current_lab.postal_code = location.raw["address"][
                "postcode"].encode('utf-8')
        current_lab.address_1 = location.address.encode('utf-8')

        # Add the lab to the list
        techshops[current_lab.slug] = current_lab

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in techshops:
            output[j] = techshops[j].__dict__
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in techshops:
            single = techshops[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return a Pandas DataFrame
    elif format.lower() == "pandas" or format.lower() == "dataframe":
        output = {}
        for j in techshops:
            output[j] = techshops[j].__dict__
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = techshops
    # Default: return an oject
    else:
        output = techshops
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)
    return output


def labs_count():
    """Gets the number of current Techshops listed on techshops.ws."""

    techshops = get_labs("object")

    return len(techshops)


if __name__ == "__main__":
    pass
