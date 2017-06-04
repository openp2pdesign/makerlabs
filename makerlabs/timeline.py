# -*- encoding: utf-8 -*-
#
# Rebuild a timeline of makerlabs
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#

# Import all the mapped platforms
import diybio_org
import fablabs_io
import makeinitaly_foundation
import hackaday_io
import hackerspaces_org
import makery_info
import nesta
import techshop_ws

import pandas as pd


def get_multiple_data():
    """Get data from all the platforms listed in makerlabs."""

    # Get data from all the mapped platforms
    all_labs = {}
    all_labs["diybio_org"] = diybio_org.get_labs(format="dict")
    all_labs["fablabs_io"] = fablabs_io.get_labs(format="dict")
    all_labs["makeinitaly_foundation"] = makeinitaly_foundation.get_labs(
        format="dict")
    all_labs["hackaday_io"] = hackaday_io.get_labs(format="dict")
    all_labs["hackerspaces_org"] = hackerspaces_org.get_labs(format="dict")
    all_labs["makery_info"] = makery_info.get_labs(format="dict")
    all_labs["nesta"] = nesta.get_labs(format="dict")
    # all_labs["techshop_ws"] = techshop_ws.get_labs(format="dict")

    return all_labs


def get_timeline(source):
    """Rebuild a timeline of the history of makerlabs."""

    # Set up the pandas timeseries dataframe
    timeline_format = ["name", "type", "source", "country", "city", "latitude",
                       "longitude", "website_url", "twitter_url",
                       "facebook_page_url", "facebook_group_url",
                       "whois_start", "whois_end", "wayback_start",
                       "wayback_end", "twitter_start", "twitter_end",
                       "facebook_start", "facebook_end"]
    timeline = pd.DataFrame(timeline_format)

    # Getdata from all the mapped platforms
    if source.lower() == "diybio.org":
        data = diybio_org.get_labs(format="dict")
    elif source.lower() == "fablabs_io":
        data = fablabs_io.get_labs(format="dict")
    elif source.lower() == "makeinitaly_foundation":
        data = makeinitaly_foundation.get_labs(format="dict")
    elif source.lower() == "hackaday_io":
        data = hackaday_io.get_labs(format="dict")
    elif source.lower() == "hackerspaces_org":
        data = hackerspaces_org.get_labs(format="dict")
    elif source.lower() == "makery_info":
        data = makery_info.get_labs(format="dict")
    elif source.lower() == "nesta":
        data = nesta.get_labs(format="dict")
    elif source.lower() == "all":
        pass

    # Fill the dataframe with basic details
    for lab in labs_data:
        for link in lab.links:
            print link
            if "twitter" in link:
                print link
            if "facebook" in link:
                print link
        lab_dataframe_dict = {"name": lab.name,
                              "type": lab.lab_type,
                              "source": lab.source,
                              "country": lab.country,
                              "city": lab.city,
                              "latitude": lab.latitude,
                              "longitude": lab.longitude,
                              "website_url": lab.url}
        timeline.append(lab_dataframe_dict)
        ["name", "type", "source", "country", "city", "lat", "long",
         "website_url", "twitter_url", "facebook_page_url",
         "facebook_group_url", "whois_start", "whois_end", "wayback_start",
         "wayback_end", "twitter_start", "twitter_end", "facebook_start",
         "facebook_end"]

    # Get time data from platforms, whenever possible

    # Get domain data (whois)

    # Get subdomain data (Internet Archive)

    # Get social media data (Twitter)

    # Get social media data (Facebook)

    return timeline


if __name__ == "__main__":
    print get_timeline("fablabs_io")
