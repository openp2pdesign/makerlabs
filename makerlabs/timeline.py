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


def get_multiple_data(format):
    """Rebuild a timeline of the history of makerlabs."""

    # Get data from all the mapped platforms
    all_labs = {}
    all_labs["diybio_org"] = diybio_org.get_labs(format=format)
    all_labs["fablabs_io"] = fablabs_io.get_labs(format=format)
    all_labs["makeinitaly_foundation"] = makeinitaly_foundation.get_labs(
        format=format)
    all_labs["hackaday_io"] = hackaday_io.get_labs(format=format)
    all_labs["hackerspaces_org"] = hackerspaces_org.get_labs(format=format)
    all_labs["makery_info"] = makery_info.get_labs(format=format)
    all_labs["nesta"] = nesta.get_labs(format=format)
    # all_labs["techshop_ws"] = techshop_ws.get_labs(format=format)

    # Here we should make the classes coherent...

    return all_labs


def get_timeline(type):
    """Rebuild a timeline of the history of makerlabs."""

    # Set up the pandas timeseries dataframe
    timeline_format = ["name", "type", "source", "country", "city", "lat",
                       "long", "website_url", "twitter_url",
                       "facebook_page_url", "facebook_group_url",
                       "whois_start", "whois_end", "wayback_start",
                       "wayback_end", "twitter_start", "twitter_end",
                       "facebook_start", "facebook_end"]
    timeline = pd.DataFrame(timeline_format)

    # Get data from all the mapped platforms
    labs_data = get_multiple_data(format="dict")

    # Fill the dataframe with basic details

    # Get time data from platforms, whenever possible

    # Get domain data (whois)

    # Get subdomain data (Internet Archive)

    # Get social media data (Twitter)

    # Get social media data (Facebook)

    return timeline


if __name__ == "__main__":
    print get_timeline("prova")
