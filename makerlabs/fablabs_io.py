# -*- encoding: utf-8 -*-
#
# Access data from fablabs.io
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#

import requests

# Endpoints
fablabs_io_labs_api_url_v0 = "https://api.fablabs.io/v0/labs.json"
fablabs_io_projects_api_url_v0 = "https://api.fablabs.io/v0/projects.json"


class FabLab(object):
    """Represents a Fab Lab as it is described on fablabs.io."""

    def __init__(self):
        self.address_1 = ""
        self.address_2 = ""
        self.address_notes = ""
        self.avatar = ""
        self.blurb = ""
        self.capabilities = ""
        self.city = ""
        self.country_code = ""
        self.county = ""
        self.description = ""
        self.email = ""
        self.header_image_src = ""
        self.id = ""
        self.kind_name = ""
        self.latitude = ""
        self.longitude = ""
        self.links = ""
        self.name = ""
        self.parent_id = ""
        self.phone = ""
        self.postal_code = ""
        self.slug = ""
        self.url = ""


def data_from_fablabs_io(endpoint):
    """Gets data from fablabs.io."""

    data = requests.get(endpoint).json()

    return data


def get_labs(format):
    """Gets FabLab data from fablabs.io."""

    fablabs_json = data_from_fablabs_io(fablabs_io_labs_api_url_v0)
    fablabs = {}

    # Load all the FabLabs
    for i in fablabs_json["labs"]:
        current_lab = FabLab()
        current_lab.address_1 = i["address_1"]
        current_lab.address_2 = i["address_2"]
        current_lab.address_notes = i["address_notes"]
        current_lab.avatar = i["avatar"]
        current_lab.blurb = i["blurb"]
        current_lab.capabilities = i["capabilities"]
        current_lab.city = i["city"]
        current_lab.country_code = i["country_code"]
        current_lab.county = i["county"]
        current_lab.description = i["description"]
        current_lab.email = i["email"]
        current_lab.header_image_src = i["header_image_src"]
        current_lab.id = i["id"]
        current_lab.kind_name = i["kind_name"]
        current_lab.latitude = i["latitude"]
        current_lab.longitude = i["longitude"]
        current_lab.links = i["links"]
        current_lab.name = i["name"]
        current_lab.parent_id = i["parent_id"]
        current_lab.phone = i["phone"]
        current_lab.postal_code = i["postal_code"]
        current_lab.slug = i["slug"]
        current_lab.url = i["url"]
        fablabs[i["slug"]] = current_lab

    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in fablabs:
            output[j] = fablabs[j].__dict__
    elif format.lower() == "object" or format.lower() == "obj":
        output = fablabs
    else:
        output = fablabs

    return output


def labs_count():
    """Gets the number of current Fab Labs registered on fablabs.io."""

    fablabs = data_from_fablabs_io(fablabs_io_labs_api_url_v0)

    return len(fablabs["labs"])


if __name__ == "__main__":
    pass
