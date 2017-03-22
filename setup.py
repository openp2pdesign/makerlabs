from distutils.core import setup
setup(
    name='makerlabs',
    packages=['makerlabs'],
    install_requires=[
        "kitchen",
        "requests",
        "mwparserfromhell",
        "simplemediawiki",
        "wsgiref",
        "geojson",
        "geopy",
        "beautifulsoup4",
        "lxml"
    ],
    version='0.15',
    description='A python library for accessing online data about Makerspaces, Fab Labs, Hackerspaces, TechShop...',
    author='Massimo Menichinelli',
    author_email='info@openp2pdesign.org',
    url='https://github.com/openp2pdesign/makerlabs',
    download_url='https://github.com/openp2pdesign/makerlabs/releases/tag/v0.15',
    keywords=['Fab Lab', 'Fab Lab', 'Makerspace', 'Hackerspace', 'TechShop',
              'Makers'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ], )
