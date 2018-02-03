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


def get_location(query, format, api_key):
    """Get geographic data of a lab in a coherent way for all labs."""

    # Play nice with the API...
    sleep(1)
    geolocator = OpenCage(api_key=api_key, timeout=10)

    # Variables for storing the data
    data = {"city": None,
            "address_1": None,
            "postal_code": None,
            "country": None,
            "county": None,
            "state": None,
            "country_code": None,
            "latitude": None,
            "longitude": None,
            "continent": None}
    road = ""
    number = ""
    # Default None values
    location_data = {"city": None,
                     "road": None,
                     "house_number": None,
                     "postcode": None,
                     "country": None,
                     "county": None,
                     "state": None,
                     "ISO_3166-1_alpha-2": None,
                     "country_code": None,
                     "lat": None,
                     "lng": None}

    # Reverse geocoding ... from coordinates to address
    if format == "reverse":
        # If the query (coordinates) is not empty
        if query is None or len(query) < 3:
            pass
        else:
            location = geolocator.reverse(query)
            if location is not None:
                location_data = location[0].raw[u'components']
                location_data["lat"] = location[0].raw[u'geometry']["lat"]
                location_data["lng"] = location[0].raw[u'geometry']["lng"]
    # Direct geocoding ... from address to coordinates and full address
    if format == "direct":
        # If the query (address) is not empty
        if query is None or len(query) < 3:
            pass
        else:
            location = geolocator.geocode(query)
            if location is not None:
                location_data = location.raw[u'components']
                location_data["lat"] = location.raw[u'geometry']["lat"]
                location_data["lng"] = location.raw[u'geometry']["lng"]

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
    # Format the country code to three letters
    try:
        country_data = transformations.cca2_to_ccn(data["country_code"])
        data["country_code"] = transformations.ccn_to_cca3(country_data)
    except:
        data["country_code"] = None
    # Get the continent
    try:
        country_data = transformations.cc_to_cn(data["country_code"])
        data["continent"] = transformations.cn_to_ctn(country_data)
    except:
        data["continent"] = None

    # Return the final data
    return data


if __name__ == "__main__":
    pass
