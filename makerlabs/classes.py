# -*- encoding: utf-8 -*-
#
# Classes
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


class Lab(object):
    """Represents a Lab with the most common fields found."""

    def __init__(self):
        self.source = ""
        self.id = ""
        self.name = ""
        self.lab_type = ""
        self.continent = ""
        self.city = ""
        self.country_code = ""
        self.country = ""
        self.address_1 = ""
        self.address_2 = ""
        self.postal_code = ""
        self.county = ""
        self.state = ""
        self.latitude = ""
        self.longitude = ""
        self.url = ""
        self.slug = ""
        self.email = ""
        self.avatar = ""
        self.blurb = ""
        self.description = ""
        self.phone = ""
        self.capabilities = ""
        self.manager = ""
        self.links = ""
        self.created_at = ""
        self.membercount = ""
        self.size = ""
        self.status = ""


class Faire(object):
    """Represents a Maker Faire with the most common fields found."""

    def __init__(self):
        self.source = ""
        self.id = ""
        self.name = ""
        self.faire_type = ""
        self.continent = ""
        self.city = ""
        self.country_code = ""
        self.country = ""
        self.address_1 = ""
        self.address_2 = ""
        self.postal_code = ""
        self.county = ""
        self.state = ""
        self.latitude = ""
        self.longitude = ""
        self.url = ""
        self.description = ""
        self.category = ""
        self.event_type = ""
        self.year = ""
        self.dt = ""
        self.event_start_dt = ""
        self.event_end_dt = ""
        self.cfm_start_dt = ""
        self.cfm_end_dt = ""
        self.free_event = ""
