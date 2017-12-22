# -*- encoding: utf-8 -*-
#
# Access data from NESTA at https://github.com/nesta-uk/UK-makerspaces
# Data license: CC Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab

import json
import pandas as pd
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim
import pandas as pd

# Geocoding variable
geolocator = Nominatim()

# Endpoints
nesta_uk_url = "https://raw.githubusercontent.com/nesta-uk/UK-makerspaces/master/ukmakerspacesidentifiabledata.csv"


class UKMakerspace(Lab):
    """Represents a UK Makerspace from the NESTA research, in a simplified way."""

    def __init__(self):
        self.source = "NESTA"
        self.lab_type = "UK Makerspace from the NESTA"
        self.continent = "Europe"
        self.country_code = "UK"
        self.country = "United Kingdom"


def data_from_nesta():
    """Read data from the GitHub repo."""

    data = pd.read_csv(nesta_uk_url)

    return data


def get_labs(format):
    """Gets current UK Makerspaces data as listed by NESTA."""

    ukmakerspaces_data = data_from_nesta()
    ukmakerspaces = {}

    # Iterate over csv rows
    for index, row in ukmakerspaces_data.iterrows():
        current_lab = UKMakerspace()
        current_lab.address_1 = row["Address"].replace("\r", " ")
        current_lab.address_2 = row["Region"].replace("\r", " ") + " - " + row["Area"].replace("\r", " ")
        current_lab.city = ""
        current_lab.county = ""
        current_lab.email = row["Email address"]
        current_lab.latitude = ""
        current_lab.longitude = ""
        current_lab.links = ""
        current_lab.name = row["Name of makerspace"]
        current_lab.phone = row["Phone number"]
        current_lab.postal_code = row["Postcode"]
        current_lab.url = row["Website / URL"]

        # Add the lab, with a slug from the name
        ukmakerspaces[current_lab.name] = current_lab

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in ukmakerspaces:
            output[j] = ukmakerspaces[j].__dict__
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in ukmakerspaces:
            single = ukmakerspaces[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return a Pandas DataFrame
    elif format.lower() == "pandas" or format.lower() == "dataframe":
        output = {}
        for j in ukmakerspaces:
            output[j] = ukmakerspaces[j].__dict__
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = ukmakerspaces
    # Default: return an oject
    else:
        output = ukmakerspaces
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)
    return output


def labs_count():
    """Gets the number of current UK Makerspaces listed by NESTA."""

    ukmakerspaces = get_labs("object")

    return len(ukmakerspaces)


if __name__ == "__main__":
    pass
