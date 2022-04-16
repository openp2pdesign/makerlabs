# -*- encoding: utf-8 -*-
#
# Access data from fablabs.io
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from .classes import Lab

import json
import requests
from geojson import dumps, Feature, Point, FeatureCollection
from geopy.geocoders import Nominatim
import pycountry
from time import sleep
import pandas as pd


# Geocoding variable
geolocator = Nominatim()

# Endpoints
fablabs_io_labs_api_url_v0 = "https://api.fablabs.io/v0/labs.json"
fablabs_io_projects_api_url_v0 = "https://api.fablabs.io/v0/projects.json"


class FabLab(Lab):
    """Represents a Fab Lab as it is described on fablabs.io."""

    def __init__(self):
        self.source = "fablabs.io"
        self.lab_type = "Fab Lab"


class Project(object):
    """Represents a project as it is described on fablabs.io."""

    def __init__(self):
        self.id = ""
        self.title = ""
        self.description = ""
        self.github = ""
        self.web = ""
        self.dropbox = ""
        self.bitbucket = ""
        self.lab_id = ""
        self.lab = ""
        self.owner_id = ""
        self.created_at = ""
        self.updated_at = ""
        self.vimeo = ""
        self.flickr = ""
        self.youtube = ""
        self.drive = ""
        self.twitter = ""
        self.facebook = ""
        self.googleplus = ""
        self.instagram = ""
        self.status = ""
        self.version = ""
        self.faq = ""
        self.scope = ""
        self.community = ""
        self.lookingfor = ""
        self.cover = ""
        self.type = "Project in a Fab Lab"


def data_from_fablabs_io(endpoint):
    """Gets data from fablabs.io."""

    data = requests.get(endpoint).json()

    return data


def get_labs(format):
    """Gets Fab Lab data from fablabs.io."""

    fablabs_json = data_from_fablabs_io(fablabs_io_labs_api_url_v0)
    fablabs = {}

    # Load all the FabLabs
    for i in fablabs_json["labs"]:
        current_lab = FabLab()
        current_lab.name = i["name"]
        current_lab.address_1 = i["address_1"]
        current_lab.address_2 = i["address_2"]
        current_lab.address_notes = i["address_notes"]
        current_lab.avatar = i["avatar_url"]
        current_lab.blurb = i["blurb"]
        current_lab.capabilities = i["capabilities"]
        if i["city"].isupper():
            i["city"] = i["city"].title()
        current_lab.city = i["city"]
        current_lab.country_code = i["country_code"]
        current_lab.county = i["county"]
        current_lab.description = i["description"]
        current_lab.email = i["email"]
        current_lab.id = i["id"]
        current_lab.phone = i["phone"]
        current_lab.postal_code = i["postal_code"]
        current_lab.slug = i["slug"]
        current_lab.url = i["url"]

        continent_code = pycountry.country_alpha2_to_continent_code(i["country_code"])
        current_lab.continent = pycountry.convert_continent_code_to_continent_name(continent_code)

        current_country = pycountry.countries.get(alpha_2=i["country_code"].upper())
        current_lab.country_code = current_country.alpha_3
        current_lab.country = current_country.name

        # Check coordinates
        if i["longitude"] is not None:
            current_lab.longitude = i["longitude"]
        else:
            current_lab.longitude = 0.0
        if i["latitude"] is not None:
            current_lab.latitude = i["latitude"]
        else:
            current_lab.latitude = 0.0

        # Find Facebook and Twitter links, add also the other ones
        current_lab.links = {"facebook": "", "twitter": ""}
        for link in i["links"]:
            if "facebook" in link["url"]:
                current_lab.links["facebook"] = link["url"]
            elif "twitter" in link["url"]:
                current_lab.links["twitter"] = link["url"]
            else:
                current_lab.links[link["id"]] = link["url"]

        # Add the lab to the list
        fablabs[i["slug"]] = current_lab

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in fablabs:
            output[j] = fablabs[j].__dict__
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in fablabs:
            single = fablabs[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return a Pandas DataFrame
    elif format.lower() == "pandas" or format.lower() == "dataframe":
        output = {}
        for j in fablabs:
            output[j] = fablabs[j].__dict__
        # Transform the dict into a Pandas DataFrame
        output = pd.DataFrame.from_dict(output)
        output = output.transpose()
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = fablabs
    # Default: return an oject
    else:
        output = fablabs
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)
    return output


def labs_count():
    """Gets the number of current Fab Labs registered on fablabs.io."""

    fablabs = data_from_fablabs_io(fablabs_io_labs_api_url_v0)

    return len(fablabs["labs"])


def get_projects(format):
    """Gets projects data from fablabs.io."""

    projects_json = data_from_fablabs_io(fablabs_io_projects_api_url_v0)
    projects = {}
    project_url = "https://www.fablabs.io/projects/"
    fablabs = get_labs(format="object")

    # Load all the FabLabs
    for i in projects_json["projects"]:
        i = i["projects"]
        current_project = Project()
        current_project.id = i["id"]
        current_project.title = i["title"]
        current_project.description = i["description"]
        current_project.github = i["github"]
        current_project.web = i["web"]
        current_project.dropbox = i["dropbox"]
        current_project.bitbucket = i["bitbucket"]
        current_project.lab_id = i["lab_id"]
        # Add the lab of the project
        if i["lab_id"] is not None:
            for k in fablabs:
                if fablabs[k].id == i["lab_id"]:
                    current_project.lab = fablabs[k]
        else:
            current_project.lab = None
        current_project.owner_id = i["owner_id"]
        current_project.created_at = i["created_at"]
        current_project.updated_at = i["updated_at"]
        current_project.vimeo = i["vimeo"]
        current_project.flickr = i["flickr"]
        current_project.youtube = i["youtube"]
        current_project.drive = i["drive"]
        current_project.twitter = i["twitter"]
        current_project.facebook = i["facebook"]
        current_project.googleplus = i["googleplus"]
        current_project.instagram = i["instagram"]
        current_project.status = i["status"]
        current_project.version = i["version"]
        current_project.faq = i["faq"]
        current_project.scope = i["scope"]
        current_project.community = i["community"]
        current_project.lookingfor = i["lookingfor"]
        current_project.cover = i["cover"]
        url = project_url + str(current_project.id)
        current_project.url = url
        # Add the project
        projects[current_project.id] = current_project

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = {}
        for j in projects:
            project_dict = projects[j].__dict__
            # Convert the lab from a Fab Lab object to a dict
            if project_dict["lab"] is not None:
                project_dict["lab"] = project_dict["lab"].__dict__
            output[j] = project_dict
    # Return a geojson, only for projects linked to a lab
    elif format.lower() == "geojson" or format.lower() == "geo":
        projects_list = []
        for p in projects:
            if projects[p].lab_id is not None:
                single_project = projects[p].__dict__
                if projects[p].lab is not None:
                    single_project["lab"] = single_project["lab"].__dict__
                for l in fablabs:
                    single_lab = fablabs[l].__dict__
                    if single_lab["id"] == single_project["lab_id"]:
                        project_lab = Feature(
                            type="Feature",
                            geometry=Point((single_lab["latitude"],
                                            single_lab["longitude"])),
                            properties=single_project)
                        projects_list.append(project_lab)
                output = dumps(FeatureCollection(projects_list))
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = projects
    # Default: return an object
    else:
        output = projects
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(output)
    return output


def projects_count():
    """Gets the number of current projects submitted on fablabs.io."""

    projects = data_from_fablabs_io(fablabs_io_projects_api_url_v0)

    return len(projects["projects"])


if __name__ == "__main__":
    print(get_labs(format="json"))
