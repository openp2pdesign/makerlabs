# -*- encoding: utf-8 -*-
#
# Access data from diybio.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from . classes import Lab
from . utils import get_location
from . utils import format_labs_data

import json
from bs4 import BeautifulSoup
import requests
import us
import pandas as pd

# Endpoints
API_endpoint = "https://diybio.org/local/"
# Plan moving to DIYbiosphere
#https://sphere.diybio.org/
#https://sphere.diybio.org/browse/?q=&idx=diybiosphere&p=0&dFR%5Bcollection%5D%5B0%5D=labs
#https://github.com/DIYbiosphere/sphere


class DiyBioLab(Lab):
    """Represents a DIYBio Lab as it is described on diybio.org."""

    def __init__(self):
        self.source = "diybio.org"
        self.lab_type = "DIYBio Lab"


def data_from_diybio_org():
    """Scrapes data from diybio.org."""

    r = requests.get(API_endpoint)

    if r.status_code == 200:
        # Fix a problem in the html source while loading it
        data = BeautifulSoup(r.text.replace('\xa0', ''), "lxml")
    else:
        data = "There was an error while accessing data on diybio.org."

    return data


def get_labs(format, open_cage_api_key):
    """Gets DIYBio Lab data from diybio.org."""

    diybiolabs_soup = data_from_diybio_org()
    diybiolabs = {}

    rows_list = []
    continents_dict = {}
    continents_order = 0
    ranges_starting_points = []

    # Load all the DIYBio Labs
    # By first parsing the html

    # Parse table rows
    for row in diybiolabs_soup.select("table tr"):
        cells = row.find_all('td')
        rows_list.append(cells)

    # Find the continents in order to iterate over their children td
    for k, row in enumerate(rows_list):
        for col in row:
            if col.find('h3'):
                for h3 in col.findAll('h3'):
                    ranges_starting_points.append(k)
                    continents_dict[continents_order] = h3.get_text()
                    continents_order += 1

    # Find the rows of each continent
    ranges = {}
    for k, j in enumerate(reversed(ranges_starting_points)):
        if k < len(ranges_starting_points) - 1:
            ranges[k] = {"start": ranges_starting_points[k],
                         "end": ranges_starting_points[k + 1]}
        else:
            # The last continent, Oceania
            ranges[k] = {"start": ranges_starting_points[k],
                         "end": len(rows_list)}

    # Iterate over the range of each continent to find the Labs
    for i in ranges:
        # The +1 just avoids the H3 line
        for j in range(ranges[i]["start"] + 1, ranges[i]["end"]):
            # Avoid empty rows by measuring the lenght of the content of each cell and with a boolean check
            rules = [len(n) == 0 for n in rows_list[j]]
            if False in rules:
                current_lab = DiyBioLab()
                current_lab.city = rows_list[j][1].contents[0].encode('utf-8')
                # Data from the USA is not really well formatted
                if continents_dict[i] == "USA-EAST" or continents_dict[
                        i] == "USA-WEST":
                    current_lab.state = rows_list[j][2].contents[0].replace(
                        " ", "").encode('utf-8')
                else:
                    current_lab.country_code = rows_list[j][2].contents[
                        0].encode('utf-8')
                current_lab.url = rows_list[j][3].contents[0].attrs['href']
                # Each lab is identified by the simplified url
                slug = current_lab.url
                if "http://" in slug:
                    slug = slug.replace("http://", "")
                elif "https://" in slug:
                    slug = slug.replace("https://", "")
                if "www." in slug:
                    slug = slug.replace("www.", "")
                current_lab.name = slug
                current_lab.slug = slug

                # Data from the USA is not really well formatted
                if continents_dict[i] == "USA-EAST" or continents_dict[i] == "USA-WEST":
                    current_lab.continent = "North America"
                    current_lab.country_code = "USA"
                    current_lab.country = "United States of America"
                    current_lab.state = us.states.lookup(
                        current_lab.state).name

                # Get address from city
                address = get_location(query=current_lab.city, format="direct", api_key=open_cage_api_key)
                current_lab.continent = address["continent"]
                current_lab.latitude = address["latitude"]
                current_lab.longitude = address["longitude"]
                current_lab.address_1 = address["address_1"]
                current_lab.country = address["country"]
                current_lab.country_code = address["country_code"]
                current_lab.latitude = address["latitude"]
                current_lab.longitude = address["longitude"]
                current_lab.county = address["county"]
                current_lab.postal_code = address["postal_code"]
                current_lab.state = address["state"]

                # Add the lab to the list
                diybiolabs[slug] = current_lab
                del current_lab

    # Return formatted data
    data = format_labs_data(format=format, labs=diybiolabs)

    return data


def labs_count():
    """Gets the number of current DIYBio Labs listed on diybio.org."""

    diybiolabs = get_labs()

    return len(diybiolabs)


if __name__ == "__main__":
    pass
