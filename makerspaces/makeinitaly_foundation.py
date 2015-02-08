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
			latlong = []
			if ", " in value:
				latlong = value.rstrip(", ").split(", ")
			elif " , " in value:
				latlong = value.rstrip(" , ").split(" , ")
			else:
				latlong = ["",""]
			currentlab.lat = latlong[0]
			currentlab.long = latlong[1]
		elif "province=" in i:
			value = i.replace("province=", "")
			currentlab.province = value.upper()
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
	
	
def get_labs():
	"""Gets data from all labs from makeinitaly.foundation."""

	wiki = MediaWiki(makeinitaly__foundation_api_url)
	wiki_response = wiki.call({'action': 'query', 'list': 'categorymembers', 'cmtitle': 'Category:Italian_FabLabs','cmlimit': '500'})
	urls = []
	for i in wiki_response["query"]["categorymembers"]:
		urls.append(i["title"].replace(" ", "_"))
	
	labs = {}
	# Load all the Labs
	for i in urls:
		current_lab = get_single_lab(i)
		labs[i] = current_lab
	
	return labs

def get_lab_dict(slug):
	"""Gets a Lab from makeinitaly.foundation as dictionariy instead of Lab object."""
	
	labdict = get_single_lab("WeMake").__dict__
		
	return labdict
	
def labs_count():
	"""Gets the number of current Labs registered on makeinitaly.foundation."""
	
	#fablabs = data_from_fablabs_io()
	
	#return len(fablabs["labs"])
	return

if __name__ == "__main__":
	# Debug
	#a = data_from_makeinitaly_foundation()
	#print a["query"]["categorymembers"]
	#b = get_lab_dict("WeMake")
	#print b
	d = get_labs()
	#a = get_fablabs()
	#print a["ouagalab"].name
	#print a["ouagalab"].city
	#b = data_from_fablabs_io()
	#c = fablabs_count()
	#print c
	#print get_fablabs_dict()