# -*- encoding: utf-8 -*-
#
# Access data from hackerspaces.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab
from utils import get_location

import json
from simplemediawiki import MediaWiki
import mwparserfromhell
import pandas as pd

hackerspaces_org_api_url = "https://wiki.hackerspaces.org/w/api.php"


class Hackerspace(Lab):

    """Represents a Hackerspace as it is described on hackerspaces.org."""

    def __init__(self):
        self.source = "hackerspaces.org"
        self.lab_type = "Hackerspace"


def get_single_lab(lab_slug, open_cage_api_key):
    """Gets data from a single lab from hackerspaces.org."""
    wiki = MediaWiki(hackerspaces_org_api_url)
    wiki_response = wiki.call(
        {'action': 'query',
         'titles': lab_slug,
         'prop': 'revisions',
         'rvprop': 'content'})

    # If we don't know the pageid...
    for i in wiki_response["query"]["pages"]:
        content = wiki_response["query"]["pages"][i]["revisions"][0]["*"]

    # Transform the data into a Lab object
    current_lab = Hackerspace()

    equipment_list = []

    # Parse the Mediawiki code
    wikicode = mwparserfromhell.parse(content)
    for k in wikicode.filter_templates():
        element_name = unicode(k.name)
        if "Hackerspace" in element_name:
            for j in k.params:
                current_lab.name = lab_slug
                j_value = unicode(j.value)
                j_name = unicode(j.name)
                # Remove new line in content
                if j_value[-1:] == "\n" or j_value[:1] == "\n":
                    j_value = j_value.replace('\n', '')
                if j_name == "logo":
                    current_lab.logo = j_value
                if j_name == "founding":
                    current_lab.founding = j_value
                if j_name == "coordinate":
                    # Clean the coordinates
                    j_value = j_value.replace('"', '')
                    j_value = j_value.replace('N', '')
                    j_value = j_value.replace('S', '')
                    j_value = j_value.replace('W', '')
                    j_value = j_value.replace('E', '')
                    j_value = j_value.replace(u'°', '')
                    j_value = j_value.replace(' ', '')
                    # Get the full address with the coordinates
                    address = get_location(query=j_value, format="reverse", api_key=open_cage_api_key)
                    current_lab.city = address["city"]
                    current_lab.county = address["county"]
                    current_lab.state = address["state"]
                    current_lab.postal_code = address["postal_code"]
                    current_lab.address_1 = address["address_1"]
                    current_lab.country = address["country"]
                    current_lab.country_code = address["country_code"]
                    current_lab.continent = address["continent"]
                    current_lab.latitude = address["latitude"]
                    current_lab.longitude = address["longitude"]
                if j_name == "membercount":
                    current_lab.membercount = j_value
                if j_name == "fee":
                    current_lab.fee = j_value
                if j_name == "size":
                    current_lab.size = j_value
                if j_name == "status":
                    current_lab.status = j_value
                if j_name == "site":
                    current_lab.site = j_value
                if j_name == "wiki":
                    current_lab.wiki = j_value
                if j_name == "irc":
                    current_lab.irc = j_value
                if j_name == "jabber":
                    current_lab.jabber = j_value
                if j_name == "phone":
                    current_lab.phone = j_value
                if j_name == "youtube":
                    current_lab.youtube = j_value
                if j_name == "eventbrite":
                    current_lab.eventbrite = j_value
                if j_name == "facebook":
                    current_lab.facebook = j_value
                if j_name == "ustream":
                    current_lab.ustream = j_value
                if j_name == "flickr":
                    current_lab.flickr = j_value
                if j_name == "twitter":
                    current_lab.twitter = j_value
                if j_name == "googleplus":
                    current_lab.googleplus = j_value
                if j_name == "email":
                    current_lab.email = j_value
                if j_name == "maillist":
                    current_lab.maillist = j_value
                if j_name == "ical":
                    current_lab.ical = j_value
                if j_name == "forum":
                    current_lab.forum = j_value
        elif "Equipment" in element_name:
            for j in k.params:
                equipment_list.append(j.replace("equipment=", ""))

            current_lab.equipment = equipment_list

    # Load the free text
    freetext = ""
    for k in wikicode._nodes:
        try:
            test_value = k.name
        except AttributeError:
            freetext += unicode(k)
    current_lab.text = freetext

    return current_lab


def get_labs(format, open_cage_api_key):
    """Gets data from all labs from hackerspaces.org."""

    labs = []

    # Get the first page of data
    wiki = MediaWiki(hackerspaces_org_api_url)
    wiki_response = wiki.call(
        {'action': 'query',
         'list': 'categorymembers',
         'cmtitle': 'Category:Hackerspace',
         'cmlimit': '500'})
    nextpage = wiki_response["query-continue"]["categorymembers"]["cmcontinue"]

    urls = []
    for i in wiki_response["query"]["categorymembers"]:
        urls.append(i["title"].replace(" ", "_"))

    # Load all the Labs in the first page
    for i in urls:
        current_lab = get_single_lab(i, open_cage_api_key)
        labs.append(current_lab)

    # Load all the Labs from the other pages
    while "query-continue" in wiki_response:
        wiki = MediaWiki(hackerspaces_org_api_url)
        wiki_response = wiki.call({'action': 'query',
                                   'list': 'categorymembers',
                                   'cmtitle': 'Category:Hackerspace',
                                   'cmlimit': '500',
                                   "cmcontinue": nextpage})

        urls = []
        for i in wiki_response["query"]["categorymembers"]:
            urls.append(i["title"].replace(" ", "_"))

        # Load all the Labs
        for i in urls:
            current_lab = get_single_lab(i, open_cage_api_key)
            labs.append(current_lab)

        if "query-continue" in wiki_response:
            nextpage = wiki_response[
                "query-continue"]["categorymembers"]["cmcontinue"]
        else:
            break

    # Transform the list into a dictionary
    labs_dict = {}
    for j, k in enumerate(labs):
        labs_dict[j] = k.__dict__

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = labs_dict
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in labs_dict:
            single = labs_dict[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return a Pandas DataFrame
    elif format.lower() == "pandas" or format.lower() == "dataframe":
        output = labs_dict
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
        output = output.set_index(['name'])
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = labs
    # Default: return an object
    else:
        output = labs
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(labs_dict)
    return output


def labs_count():
    """Gets the number of current Hackerspaces registered on hackerspaces.org."""

    labs = get_labs()

    return len(labs)


if __name__ == "__main__":
    pass
