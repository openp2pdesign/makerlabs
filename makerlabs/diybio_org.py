# -*- encoding: utf-8 -*-
#
# Access data from diybio.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from bs4 import BeautifulSoup
import requests
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim


# Geocoding variable
geolocator = Nominatim()

# Endpoints
diy_bio_labs_url = "https://diybio.org/local/"


class DiyBioLab(object):
    """Represents a DIYBio Lab as it is described on diybio.org."""

    def __init__(self):
        self.continent = ""
        self.city = ""
        self.country_code = ""
        self.country = ""
        self.url = ""
        self.latitude = ""
        self.longitude = ""


def data_from_diybio_org():
    """Scrapes data from diybio.org."""

    r = requests.get(diy_bio_labs_url)
    if r.status_code == 200:
        data = BeautifulSoup(r.text, "lxml")
    else:
        data = "There was an error while accessing data on diybio.org."

    return data


def get_labs(format):
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
                current_lab.continent = continents_dict[i]
                for cell in rows_list[j]:
                    # Avoid empty cells
                    if len(cell.contents) > 0:
                        # If it is a cell with a link
                        try:
                            current_lab.url = cell.contents[0].attrs['href']
                        # Otherwise the cell has the city name or country code
                        except:
                            if len(cell.contents[0]) < 3:
                                current_lab.country_code = cell.contents[0]
                            else:
                                current_lab.city = cell.contents[0]
                                # Labs do not have coordinates
                                # so let's get them from the city name
                                # sand get the full country name from the code
                                try:
                                    location = geolocator.geocode(
                                        current_lab.city)
                                    current_lab.latitude = location.latitude
                                    current_lab.longitude = location.longitude
                                    country = geolocator.reverse(
                                        [location.latitude, location.longitude
                                         ])
                                    current_lab.country = country.raw[
                                        'address']['country']
                                except:
                                    # For labs without a city
                                    # add 0,0 as coordinates
                                    current_lab.latitude = 0.0
                                    current_lab.longitude = 0.0

                # Add the lab, with a slug from the url
                if "http://www." in current_lab.url:
                    slug = current_lab.url.replace("http://www.", "")
                elif "https://www." in current_lab.url:
                    slug = current_lab.url.replace("https://www.", "")
                diybiolabs[slug] = current_lab

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in diybiolabs:
            output[j] = diybiolabs[j].__dict__
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in diybiolabs:
            single = diybiolabs[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = diybiolabs
    # Default: return an oject
    else:
        output = diybiolabs

    return output


def labs_count():
    """Gets the number of current DIYBio Labs listed on diybio.org."""

    diybiolabs = get_labs("object")

    return len(diybiolabs)


if __name__ == "__main__":
    pass
