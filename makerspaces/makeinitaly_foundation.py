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
#Requirement: kitchen

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
		

def get_single_lab(lab_slug):
	"""Gets data from a single lab from makeinitaly.foundation."""
	wiki = MediaWiki(makeinitaly__foundation_api_url)
	wiki_response = wiki.call({'action': 'query', 'titles':lab_slug, 'prop': 'revisions', 'rvprop': 'content'})
	
	# If we don't know the pageid...
	for i in wiki_response["query"]["pages"]:
		content = wiki_response["query"]["pages"][i]["revisions"][0]["*"]
	
	# Clean the resulting string/list
	newstr01 = content.replace("}}", "")
	newstr02 = newstr01.replace("{{", "")
	result = newstr02.rstrip("\n|").split("\n|")
	result.remove(u'FabLab')
	
	# Transform the data into a Lab object
	currentlab = Lab()
	currentlab.coordinates = ""
	currentlab.long = ""
	currentlab.lat = ""
	currentlab.province = ""
	currentlab.region = ""
	currentlab.address = ""
	currentlab.city = ""
	currentlab.fablabsio = ""
	currentlab.website = ""
	currentlab.facebook = ""
	currentlab.twitter = ""
	currentlab.email = ""
	currentlab.manager = ""
	currentlab.birthyear = ""
	
	# Add existing data
	for i in result:
		if "coordinates=" in i:
			value = i.replace("coordinates=", "")
			currentlab.coordinates = value
			latlong = value.rstrip(", ").split(", ")
			currentlab.lat = latlong[0]
			currentlab.long = latlong[1]
		elif "province=" in i:
			value = i.replace("province=", "")
			currentlab.province = value
		elif "region=" in i:
			value = i.replace("region=", "")
			currentlab.region = value
		elif "address=" in i:
			value = i.replace("address=", "")
			currentlab.address = value
		elif "city=" in i:
			value = i.replace("city=", "")
			currentlab.city = value
		elif "fablabsio=" in i:
			value = i.replace("fablabsio=", "")
			currentlab.fablabsio = value
		elif "website=" in i:
			value = i.replace("website=", "")
			currentlab.website = value
		elif "facebook=" in i:
			value = i.replace("facebook=", "")
			currentlab.facebook = value
		elif "twitter=" in i:
			value = i.replace("twitter=", "")
			currentlab.twitter = value
		elif "email=" in i:
			value = i.replace("email=", "")
			currentlab.email = value
		elif "manager=" in i:
			value = i.replace("manager=", "")
			currentlab.manager = value
		elif "birthyear=" in i:
			value = i.replace("birthyear=", "")
			currentlab.birthyear = value

	return currentlab


def data_from_makeinitaly_foundation():
	"""Gets data from all labs from makeinitaly.foundation."""
	
	wiki = MediaWiki(makeinitaly__foundation_api_url)
	wiki_response = wiki.call({'action': 'query', 'list': 'categorymembers', 'cmtitle': 'Category:Italian_FabLabs','cmlimit': '500'})
	for i in wiki_response["query"]["categorymembers"]:
		print i["title"].replace(" ", "%20");
	
	return wiki_response
	
	
def get_fablabs():
	"""Gets FabLab data from fablabs.io."""

	fablabs_json = data_from_fablabs_io()
	fablabs = {}
	
	# Load all the FabLabs
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
	
	return fablabs

def get_lab_dict(slug):
	"""Gets a Lab from makeinitaly.foundation as dictionariy instead of Lab object."""
	
	labdict = get_single_lab("WeMake").__dict__
		
	return labdict

def get_fablabs_dict():
	"""Gets the Fab Labs from fablabs.io as dictionaries instead of FabLab objects."""
	fablab_data = get_fablabs()
	fablabs = {}
	
	# Load all the FabLabs
	for i in fablab_data:
		fablabs[i] = fablab_data[i].__dict__
		
	return fablabs
	
def fablabs_count():
	"""Gets the number of current Fab Labs registered on fablabs.io."""
	
	fablabs = data_from_fablabs_io()
	
	return len(fablabs["labs"])


if __name__ == "__main__":
	# Debug
	#a = data_from_makeinitaly_foundation()
	#print a["query"]["categorymembers"]
	b = get_lab_dict("WeMake")
	print b
	#a = get_fablabs()
	#print a["ouagalab"].name
	#print a["ouagalab"].city
	#b = data_from_fablabs_io()
	#c = fablabs_count()
	#print c
	#print get_fablabs_dict()