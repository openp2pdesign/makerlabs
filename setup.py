#from distutils.core import setup
from setuptools import setup
setup(
    name='makerlabs',
    packages=['makerlabs'],
    install_requires=[
        "kitchen",
        "requests",
        "wsgiref",
        "geojson",
        "geopy",
        "beautifulsoup4",
        "lxml",
        "pandas",
        "us",
        "pycountry"
    ],
    version='0.23.0',
    description='A python library for accessing online data about Makerspaces, Fab Labs, Hackerspaces, TechShop...',
    author='Massimo Menichinelli',
    author_email='info@openp2pdesign.org',
    url='https://github.com/openp2pdesign/makerlabs',
    download_url='https://github.com/openp2pdesign/makerlabs/releases/tag/v0.21.2',
    keywords=['Fab Lab', 'Fab Lab', 'Makerspace', 'Hackerspace', 'Repair Cafes',
              'Makers'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ], )
