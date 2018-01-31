# -*- encoding: utf-8 -*-
#
# Fuctions for the other modules
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#

# Import necessary modules

from geopy.geocoders import OpenCage
from time import sleep
from incf.countryutils import transformations


def get_reverse_location(coordinates, api_key):
    """Get geographic data of a lab in a coherent way for all labs."""

    # Play nice with the API...
    sleep(2)

    # Get the data
    geolocator = OpenCage(api_key=api_key, timeout=10)
    location = geolocator.reverse(coordinates)

    # Variables for storing the data
    data = {}
    road = ""
    number = ""

    # Extract the meaningful data
    for component in location[0].raw[u'components']:
        if component == "town" or component == "city":
            data["city"] = location[0].raw[u'components'][component]
        else:
            data["city"] = None
        if component == "road":
            road = location[0].raw[u'components'][component]
        if component == "house_number":
            number = location[0].raw[u'components'][component]
        if component == "postcode":
            data["postal_code"] = location[0].raw[u'components'][component]
        else:
            data["postal_code"] = None
        if component == "country":
            data["country"] = location[0].raw[u'components'][component]
        else:
            data["country"] = None
        if component == "county":
            data["county"] = location[0].raw[u'components'][component]
        else:
            data["county"] = None
        if component == "state":
            data["state"] = location[0].raw[u'components'][component]
        else:
            data["state"] = None
        if component == "ISO_3166-1_alpha-2":
            data["country_code"] = location[0].raw[u'components'][component]
        else:
            data["country_code"] = None
        # The address need to be reconstructed
        data["address_1"] = road + " " + number
        # Get the continent
        try:
            data["continent"] = transformations.cn_to_ctn(data["country"])
        except Exception as e:
            data["continent"] = None

    return data


def get_direct_location(query, api_key):
    """Get geographic data of a lab in a coherent way for all labs."""

    # Play nice with the API...
    sleep(2)

    # Get the data
    geolocator = OpenCage(api_key=api_key, timeout=10)
    location = geolocator.geocode(query)

    # Variables for storing the data
    data = {}
    road = ""
    number = ""

    # Extract the meaningful data
    for component in location.raw[u'components']:
        if component == "town" or component == "city":
            data["city"] = location.raw[u'components'][component]
        else:
            data["city"] = None
        if component == "road":
            road = location.raw[u'components'][component]
        if component == "house_number":
            number = location.raw[u'components'][component]
        if component == "postcode":
            data["postal_code"] = location.raw[u'components'][component]
        else:
            data["postal_code"] = None
        if component == "country":
            data["country"] = location.raw[u'components'][component]
        else:
            data["country"] = None
        if component == "county":
            data["county"] = location.raw[u'components'][component]
        else:
            data["county"] = None
        if component == "state":
            data["state"] = location.raw[u'components'][component]
        else:
            data["state"] = None
        if component == "ISO_3166-1_alpha-2":
            data["country_code"] = location.raw[u'components'][component]
        else:
            data["country_code"] = None
        # The address need to be reconstructed
        data["address_1"] = road + " " + number
        data["latitude"] = location.raw[u'geometry']["lat"]
        data["longitude"] = location.raw[u'geometry']["lng"]
        # Get the continent
        try:
            data["continent"] = transformations.cn_to_ctn(data["country"])
        except Exception as e:
            data["continent"] = None

    return data


if __name__ == "__main__":
    pass
