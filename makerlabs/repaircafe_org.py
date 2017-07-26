# -*- encoding: utf-8 -*-
#
# Access data from repaircafe.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#

import json
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim
import pycountry
from pycountry_convert import convert_country_alpha2_to_continent
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# Geocoding variable
geolocator = Nominatim()

# Endpoints
fablabs_io_labs_api_url_v0 = "https://api.fablabs.io/v0/labs.json"
fablabs_io_projects_api_url_v0 = "https://api.fablabs.io/v0/projects.json"


class RepairCafe(object):
    """Represents a Repair Cafe as it is described on repaircafe.org."""

    def __init__(self):
        self.source = "repaircafe.org"
        self.id = ""
        self.name = ""
        self.lab_type = "Repair Cafe"
        self.continent = ""
        self.city = ""
        self.country_code = ""
        self.country = ""
        self.address_1 = ""
        self.address_2 = ""
        self.postal_code = ""
        self.county = ""
        self.state = ""
        self.latitude = ""
        self.longitude = ""
        self.url = ""
        self.slug = ""
        self.email = ""
        self.avatar = ""
        self.blurb = ""
        self.description = ""
        self.phone = ""
        self.capabilities = ""
        self.manager = ""
        self.founding = ""
        self.links = ""


def data_from_repaircafe_org():
    """Gets data from repaircafe_org."""

    # Use Chrome as a browser
    # browser = webdriver.Chrome()
    # Use PhantomJS as a browser
    browser = webdriver.PhantomJS('phantomjs')
    browser.get("https://repaircafe.org/en/?s=Contact+the+local+organisers")
    browser.maximize_window()

    # Iterate over results (the #viewmore_link button)
    viewmore_button = True
    while viewmore_button:
        try:
            viewmore = browser.find_element_by_id("viewmore_link")
            # Scroll to the link in order to make it visible
            browser.execute_script("arguments[0].scrollIntoView();", viewmore)
            # Keep searching
            viewmore.click()
        except:
            # If there's an error, we have reached the end of the search
            viewmore_button = False
        # Give a bit of time for loading the search results
        sleep(2)

    # Load the source code
    page_source = BeautifulSoup(browser.page_source, "lxml")
    # Close the browser
    browser.quit()
    # Parse the source code in order to find all the links under H4s
    data = []
    for h4 in page_source.find_all("h4"):
        for a in h4.find_all('a', href=True):
            data.append({"name": a.contents[0], "url": a['href']})

    return data


def get_labs(format):
    """Gets Repair Cafe data from repairecafe.org."""

    data = data_from_repaircafe_org()

    repaircafes = {}

    # Load all the Repair Cafes
    for i in data:
        # Create a lab
        current_lab = RepairCafe()
        # Add existing data from first scraping
        current_lab.name = i["name"]
        slug = i["url"].replace("https://repaircafe.org/locations/", "")
        if slug.endswith("/"):
            slug.replace("/", "")
        current_lab.slug = slug
        current_lab.url = i["url"]
        # Scrape for more data
        page_request = requests.get(i["url"])
        if page_request.status_code == 200:
            page_source = BeautifulSoup(page_request.text, "lxml")
        else:
            output = "There was an error while accessing data on repaircafe.org."

        columns = page_source.find_all("div", class_="sc_column_item_2")
        for j in columns:
            print j
            for a in j.find_all('a', href=True):
                print a.contents[0], a['href']

        exit()

        current_lab.links = i["id"]
        current_lab.address_1 = i["address_1"]
        current_lab.address_2 = i["address_2"]
        current_lab.address_notes = i["address_notes"]
        current_lab.blurb = i["blurb"]
        current_lab.city = i["city"]
        current_lab.country_code = i["country_code"]
        current_lab.county = i["county"]
        current_lab.description = i["description"]
        current_lab.email = i["email"]
        current_lab.id = i["id"]
        current_lab.phone = i["phone"]
        current_lab.postal_code = i["postal_code"]


        current_lab.continent = convert_country_alpha2_to_continent(i[
            "country_code"].upper())
        current_country = pycountry.countries.get(
            alpha_2=i["country_code"].upper())
        current_lab.country_code = current_country.alpha_3
        current_lab.country = current_country.name

        if i["longitude"] is None or i["latitude"] is None:
            # Be nice with the geocoder API limit
            errorsb += 1
            # sleep(10)
            # location = geolocator.geocode(
            #     {"city": i["city"],
            #      "country": i["country_code"].upper()},
            #     addressdetails=True,
            #     language="en")
            # if location is not None:
            #     current_lab.latitude = location.latitude
            #     current_lab.longitude = location.longitude
            #     if "county" in location.raw["address"]:
            #         current_lab.county = location.raw["address"][
            #             "county"].encode('utf-8')
            #     if "state" in location.raw["address"]:
            #         current_lab.state = location.raw["address"][
            #             "state"].encode('utf-8')
        else:
            # Be nice with the geocoder API limit
            sleep(10)
            errorsa += 1
            # location = geolocator.reverse((i["latitude"], i["longitude"]))
            # if location is not None:
            #     if "county" in location.raw["address"]:
            #         current_lab.county = location.raw["address"][
            #             "county"].encode('utf-8')
            #     if "state" in location.raw["address"]:
            #         current_lab.state = location.raw["address"][
            #             "state"].encode('utf-8')

        # Find Facebook and Twitter links, add also the other ones
        current_lab.links = {"facebook": "", "twitter": ""}
        for link in i["links"]:
            if "facebook" in link["url"]:
                current_lab.links["facebook"] = link["url"]
            elif "twitter" in link["url"]:
                current_lab.links["twitter"] = link["url"]
            else:
                current_lab.links[link["id"]] = link["url"]

        # Add the lab to the list
        repaircafes[i["slug"]] = current_lab
    print "errorsa", errorsa
    print "errorsb", errorsb
    exit()
    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in repaircafes:
            output[j] = repaircafes[j].__dict__
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in repaircafes:
            single = repaircafes[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = repaircafes
    # Default: return an oject
    else:
        output = repaircafes
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)
    return output


def labs_count():
    """Gets the number of current Repair Cafes registered on repaircafe.org."""

    repaircafes = data_from_repaircafe_org()

    return len(repaircafes["labs"])


if __name__ == "__main__":
    print get_labs(format="json")
