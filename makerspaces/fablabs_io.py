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

fablabs_io_api_url = "https://api.fablabs.io/v0/labs.json"


class FabLab(object):
	"""Represents a Fab Lab as it is described on fablabs.io."""
	
	def __init__(self, address_1, address_2, address_notes, avatar, blurb, capabilities, city, country_coude, county, description, email, header_image_src, id, kind_name, latitude, longitude, links, name, parent_id, phone, postal_code, slug, url):
		self.address_1 = address_1
		self.address_2 = address_2
		self.address_notes = address_notes
		self.avatar = avatar
		self.blurb = blurb
		self.capabilities = capabilities
		self.city = city
		self.country_code = country_code
		self.county = county
		self.description = description
		self.email = email
		self.header_image_src = header_image_src
		self.id = id
		self.kind_name = kind_name
		self.latitude = latitude
		self.longitude = longitude
		self.links = links
		self.name = name
		self.parent_id = parent_id
		self.phone = phone
		self.postal_code = postal_code
		self.slug = slug
		self.url = url
        
	
        
     
def data_from_fablabs_io():
	"""Gets data from fablabs.io."""

	fablab_list = requests.get(fablabs_io_api_url).json()
	
	return fablab_list

	
def fablabs_count():
	"""Gets the number of current Fab Labs registered on fablabs.io."""
	
	fablabs = data_from_fablabs_io()
	
	return len(fablabs["labs"])


if __name__ == "__main__":
	print fablabs_count()