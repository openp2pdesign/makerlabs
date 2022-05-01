# -*- encoding: utf-8 -*-
#
# Access data from repaircafe.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab
from utils import get_location
from utils import format_labs_data

import json
import requests
import re
from geojson import dumps, Feature, Point, FeatureCollection
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd


# Endpoints
API_endpoint = "https://www.repaircafe.org/en/wp-json/wp/v2/pages/165"


class RepairCafe(Lab):
    """Represents a Repair Cafe as it is described on repaircafe.org."""

    def __init__(self):
        self.source = "repaircafe.org"
        self.lab_type = "Repair Cafe"


def data_from_repaircafe_org():
    """Gets data from repaircafe_org."""

    req = requests.get(API_endpoint).json()
    rendered = req["content"]["rendered"]
    soup = BeautifulSoup(rendered, 'lxml')
    scripts = soup.find_all('script')
    # Get locations
    pattern = re.compile('.*var locations = (.*?);.*', re.DOTALL)
    locations = []
    for script in scripts:
        script2 = script.string
        script2.replace("&amp;", "&")
        script2.replace("\u00e9", "é")
        data = pattern.match(str(script2.string))
        if data:
            locations = data.groups()[0]
    # Get titles
    pattern2 = re.compile('.*var titles = (.*?);.*', re.DOTALL)
    titles = []
    for script in scripts:
        script2 = str(script.string)
        script2 = script2.replace("&amp;", "&")
        data = pattern2.match(script2)
        if data:
            titles = data.groups()[0]
    # Get markers_content
    pattern3 = re.compile('.*var markers_content = (.*?)var poi.*', re.DOTALL)
    markers_content = []
    for script in scripts:
        script2 = str(script.string)
        script2 = script2.replace("&amp;", "&")
        data = pattern3.match(script2)
        if data:
            markers_content = data.groups()[0]
    markers_content = markers_content.replace("];", "]")
    # Load the gathered data
    locations_data = json.loads(locations)
    titles_data = json.loads(titles)
    markers_content_data = json.loads(markers_content)
    # Organize data of each lab
    data = {}
    for k,i in enumerate(titles_data):
        soupj = BeautifulSoup(markers_content_data[k], "lxml")
        pa = soupj.find_all('a', href=True)
        for a in pa:
            ja = a['href']
        ps = soupj.find_all('p')
        for s in ps:
            js = re.sub(r'\s', ' ', s.getText())
            js = js.replace('    ', ' ')
            js = js.replace('  ', '')
            js = js[1:]
        data[i] = {"title": i, 'location': locations_data[k], 'slug': ja, 'Address': js}
    # Query data of each lab
    for i in data:
        lab_req = requests.get(data[i]["slug"])
        soup = BeautifulSoup(lab_req.text, "lxml")
        # Get website url
        cy = soup.select('.field_website .data a')
        for c in cy:
            data[i]["url"] = c["href"]
        # Get Twitter url
        cy = soup.select('.field_twitter .data a')
        for c in cy:
            data[i]["twitter"] = c["href"]
        # Get Facebook url
        cy = soup.select('.field_facebook .data a')
        for c in cy:
            data[i]["facebook"] = c["href"]
        # Get description
        cy = soup.select('.field_informatie .data p')
        for c in cy:
            data[i]["description"] = c.text

    return data


def get_labs(format, open_cage_api_key):
    """Gets Repair Cafe data from repairecafe.org."""

    data = data_from_repaircafe_org()

    repaircafes = {}

    # Load all the Repair Cafes
    for i in data:
        print(i)
        exit()
        # Create a lab
        current_lab = RepairCafe()
        # Add existing data from first scraping
        current_lab.name = i["name"]

        # Add the lab to the list
        repaircafes[slug] = current_lab

    # Return formatted data
    data = format_labs_data(format=format, labs=repaircafes)

    return data


def labs_count():
    """Gets the number of current Repair Cafes registered on repaircafe.org."""

    # Request directly the number of labs as the full data takes time
    req = requests.get(API_endpoint).json()
    rendered = req["content"]["rendered"]
    soup = BeautifulSoup(rendered, 'lxml')
    scripts = soup.find_all('script')
    # Get titles
    pattern2 = re.compile('.*var titles = (.*?);.*', re.DOTALL)
    titles = []
    for script in scripts:
        script2 = str(script.string)
        script2 = script2.replace("&amp;", "&")
        data = pattern2.match(script2)
        if data:
            titles = data.groups()[0]

    repaircafes = json.loads(titles)

    return len(repaircafes)


if __name__ == "__main__":
    a = labs_count()
    print(a)
