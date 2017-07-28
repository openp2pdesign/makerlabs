# makerAPI
A python library for accessing online data about Makerspaces, Fab Labs, Hackerspaces, TechShop... and for formatting the data in order to give a unified API for understanding Maker platforms.

## How to use

Install it from [pypi](https://pypi.python.org/pypi/makerAPI/):
`pip install makerAPI`

Import a module of the package: `from makerAPI import fablabs_io`

Get, for example, the labs: `labs_data = fablabs_io.get_labs(format="dict")`

Full documentation at [http://makerlabs.readthedocs.io/en/latest/](http://makerlabs.readthedocs.io/en/latest/)

## History
This package continues the development of the discontinued packages *makerlabs* and *PyMakerspaces* at [https://pypi.python.org/pypi/makerlabs/](https://pypi.python.org/pypi/makerlabs/) and [https://pypi.python.org/pypi/PyMakerspaces/](https://pypi.python.org/pypi/PyMakerspaces/). The name was changed taking inspiration from [http://artsapi.com/](ArtsAPI) and [http://www.urbanapi.eu/](UrbanAPI) and in order to reflect the introduction of a more structured development strategy.
