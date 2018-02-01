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


def get_rlocation(query, format, api_key):
    """Get geographic data of a lab in a coherent way for all labs."""

    # Play nice with the API...
    sleep(1)

    # Get the data
    # try:
    if coordinates is None or len(coordinates) < 3:
        location_data = {"city": None, "road": None, "house_number": None, "postcode": None, "country": None, "county": None, "state": None, "ISO_3166-1_alpha-2": None, "country_code": None, "lat": None, "lng": None}
    else:
        geolocator = OpenCage(api_key=api_key, timeout=10)
        location = geolocator.reverse(coordinates)
        # Default None values
        location_data = {"city": None, "road": None, "house_number": None, "postcode": None, "country": None, "county": None, "state": None, "ISO_3166-1_alpha-2": None, "country_code": None, "lat": None, "lng": None}
        if location is not None:
            location_data = location[0].raw[u'components']
            location_data["lat"] = location[0].raw[u'geometry']["lat"]
            location_data["lng"] = location[0].raw[u'geometry']["lng"]

    # Variables for storing the data
    data = {"city": None, "address_1": None, "postal_code": None, "country": None, "county": None, "state": None, "country_code": None, "latitude": None, "longitude": None, "continent": None}
    road = ""
    number = ""

    # Extract the meaningful data
    for component in location_data:
        if component == "town" or component == "city":
            data["city"] = location_data[component]
        if component == "road":
            road = location_data[component]
        if component == "house_number":
            number = location_data[component]
        if component == "postcode":
            data["postal_code"] = location_data[component]
        if component == "country":
            data["country"] = location_data[component]
        if component == "county":
            data["county"] = location_data[component]
        if component == "state":
            data["state"] = location_data[component]
        if component == "ISO_3166-1_alpha-2":
            data["country_code"] = location_data[component]
    # The address need to be reconstructed
    data["address_1"] = unicode(road) + " " + unicode(number)
    data["latitude"] = location_data["lat"]
    data["longitude"] = location_data["lng"]
    # Get the continent
    try:
        country_data = transformations.cc_to_cn(data["country_code"])
        data["continent"] = transformations.cn_to_ctn(country_data)
    except Exception as e:
        data["continent"] = None

    return data


def get_direct_location(query, api_key):
    """Get geographic data of a lab in a coherent way for all labs."""

    # Play nice with the API...
    sleep(2)

    # Get the data
    try:
        geolocator = OpenCage(api_key=api_key, timeout=10)
        location = geolocator.geocode(query)
        location_data = location.raw[u'components']
        location_data["lat"] = location.raw[u'geometry']["lat"]
        location_data["lng"] = location.raw[u'geometry']["lng"]
    except Exception as e:
        location_data = {"city": None, "road": None, "house_number": None, "postcode": None, "country": None, "county": None, "state": None, "ISO_3166-1_alpha-2": None, "country_code": None, "lat": None, "lng": None}


    # Variables for storing the data
    data = {}
    road = ""
    number = ""

    # Extract the meaningful data
    for component in location_data:
        if component == "town" or component == "city":
            data["city"] = location_data[component]
        else:
            data["city"] = None
        if component == "road":
            road = location_data[component]
        if component == "house_number":
            number = location_data[component]
        if component == "postcode":
            data["postal_code"] = location_data[component]
        else:
            data["postal_code"] = None
        if component == "country":
            data["country"] = location_data[component]
        else:
            data["country"] = None
        if component == "county":
            data["county"] = location_data[component]
        else:
            data["county"] = None
        if component == "state":
            data["state"] = location_data[component]
        else:
            data["state"] = None
        if component == "ISO_3166-1_alpha-2":
            data["country_code"] = location_data[component]
        else:
            data["country_code"] = None
    # The address need to be reconstructed
    data["address_1"] = unicode(road) + " " + unicode(number)
    data["latitude"] = location_data["lat"]
    data["longitude"] = location_data["lng"]
    # Get the continent
    try:
        data["continent"] = transformations.cn_to_ctn(data["country"])
    except Exception as e:
        data["continent"] = None

    return data


if __name__ == "__main__":
    pass
