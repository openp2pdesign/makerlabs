#from distutils.core import setup
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='makerlabs',
    packages=['makerlabs'],
    install_requires=[
        "bs4",
        "certifi",
        "charset-normalizer",
        "geographiclib",
        "geojson",
        "geopy",
        "idna",
        "jellyfish",
        "lxml",
        "numpy",
        "pandas",
        "pathlib",
        "pycountry",
        "python-dateutil",
        "pytz",
        "requests",
        "six",
        "soupsieve",
        "urllib3",
        "us"
    ],
    version='0.31',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Massimo Menichinelli',
    author_email='info@openp2pdesign.org',
    url='https://github.com/openp2pdesign/makerlabs',
    download_url='https://github.com/openp2pdesign/makerlabs/releases/tag/v0.31',
    keywords=['Fab Lab', 'Fab Lab', 'Makerspace', 'Hackerspace', 'Repair Cafes',
              'Makers', 'DIYbio'],
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
