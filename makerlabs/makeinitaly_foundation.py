# -*- encoding: utf-8 -*-
#
# Access data from makeinitaly.foundation
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from simplemediawiki import MediaWiki


makeinitaly__foundation_api_url = "http://makeinitaly.foundation/wiki/api.php"


class Lab(object):

    """Represents a Lab as it is described on makeinitaly.foundation."""

    def __init__(self):
        self.long = ""
        self.lat = ""
        self.coordinates = ""
        self.province = ""
        self.region = ""
        self.address = ""
        self.city = ""
        self.fablabsio = ""
        self.website = ""
        self.facebook = ""
        self.twitter = ""
        self.email = ""
        self.manager = ""
        self.birthyear = ""
        self.text_it = ""
        self.text_en = ""


def get_lab_text(lab_slug, language):
    """Gets text description in English or Italian from a single lab from makeinitaly.foundation."""
    if language == "English" or language == "english" or language == "EN" or language == "En":
        language = "en"
    elif language == "Italian" or language == "italian" or language == "IT" or language == "It" or language == "it":
        language = "it"
    else:
        language = "en"
    wiki = MediaWiki(makeinitaly__foundation_api_url)
    wiki_response = wiki.call(
        {'action': 'query',
         'titles': lab_slug + "/" + language,
         'prop': 'revisions',
         'rvprop': 'content'})

    # If we don't know the pageid...
    for i in wiki_response["query"]["pages"]:
        if "revisions" in wiki_response["query"]["pages"][i]:
            content = wiki_response["query"]["pages"][i]["revisions"][0]["*"]
        else:
            content = ""

    # Clean the resulting string/list
    newstr01 = content.replace("}}", "")
    newstr02 = newstr01.replace("{{", "")
    result = newstr02.rstrip("\n|").split("\n|")

    return result[0]


def get_single_lab(lab_slug, data_format):
    """Gets data from a single lab from makeinitaly.foundation."""
    wiki = MediaWiki(makeinitaly__foundation_api_url)
    wiki_response = wiki.call(
        {'action': 'query',
         'titles': lab_slug,
         'prop': 'revisions',
         'rvprop': 'content'})

    # If we don't know the pageid...
    for i in wiki_response["query"]["pages"]:
        content = wiki_response["query"]["pages"][i]["revisions"][0]["*"]

    # Clean the resulting string/list
    newstr01 = content.replace("}}", "")
    newstr02 = newstr01.replace("{{", "")
    result = newstr02.rstrip("\n|").split("\n|")
    # result.remove(u'FabLab')

    # Transform the data into a Lab object
    current_lab = Lab()

    # Add existing data
    for i in result:
        if "coordinates=" in i:
            value = i.replace("coordinates=", "")
            current_lab.coordinates = value
            latlong = []
            if ", " in value:
                latlong = value.rstrip(", ").split(", ")
            elif " , " in value:
                latlong = value.rstrip(" , ").split(" , ")
            else:
                latlong = ["", ""]
            current_lab.lat = latlong[0]
            current_lab.long = latlong[1]
        elif "province=" in i:
            value = i.replace("province=", "")
            current_lab.province = value.upper()
        elif "region=" in i:
            value = i.replace("region=", "")
            current_lab.region = value
        elif "address=" in i:
            value = i.replace("address=", "")
            current_lab.address = value
        elif "city=" in i:
            value = i.replace("city=", "")
            current_lab.city = value
        elif "fablabsio=" in i:
            value = i.replace("fablabsio=", "")
            current_lab.fablabsio = value
        elif "website=" in i:
            value = i.replace("website=", "")
            current_lab.website = value
        elif "facebook=" in i:
            value = i.replace("facebook=", "")
            current_lab.facebook = value
        elif "twitter=" in i:
            value = i.replace("twitter=", "")
            current_lab.twitter = value
        elif "email=" in i:
            value = i.replace("email=", "")
            current_lab.email = value
        elif "manager=" in i:
            value = i.replace("manager=", "")
            current_lab.manager = value
        elif "birthyear=" in i:
            value = i.replace("birthyear=", "")
            current_lab.birthyear = value

    current_lab.text_en = get_lab_text(lab_slug=lab_slug, language="en")
    current_lab.text_it = get_lab_text(lab_slug=lab_slug, language="it")

    if data_format == "dict":
        return current_lab.__dict__
    elif data_format == "object":
        return current_lab


def get_labs(data_format):
    """Gets data from all labs from makeinitaly.foundation."""

    labs = []

    # Get the first page of data
    wiki = MediaWiki(makeinitaly__foundation_api_url)
    wiki_response = wiki.call(
        {'action': 'query',
         'list': 'categorymembers',
         'cmtitle': 'Category:Italian_FabLabs',
         'cmlimit': '500'})
    if "query-continue" in wiki_response:
        nextpage = wiki_response[
            "query-continue"]["categorymembers"]["cmcontinue"]

    urls = []
    for i in wiki_response["query"]["categorymembers"]:
        urls.append(i["title"].replace(" ", "_"))

    # Load all the Labs in the first page
    for i in urls:
        current_lab = get_single_lab(i, data_format)
        labs.append(current_lab)

    # Load all the Labs from the other pages
    while "query-continue" in wiki_response:
        wiki = MediaWiki(makeinitaly__foundation_api_url)
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
            current_lab = get_single_lab(i, data_format)
            labs.append(current_lab)

        if "query-continue" in wiki_response:
            nextpage = wiki_response[
                "query-continue"]["categorymembers"]["cmcontinue"]
        else:
            break

    # Transform the list into a dictionary
    labs_dict = {}
    for j, k in enumerate(labs):
        labs_dict[j] = k

    return labs_dict


def labs_count():
    """Gets the number of current Labs registered on makeinitaly.foundation."""

    labs = get_labs(data_format="dict")

    return len(labs)


if __name__ == "__main__":
    pass
