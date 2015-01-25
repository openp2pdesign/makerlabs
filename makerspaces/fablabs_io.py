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