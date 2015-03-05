from distutils.core import setup
setup(
  name = 'PyMakerspaces',
  packages = ['makerspaces'],
  install_requires=[
  		"kitchen",
        "requests",
        "mwparserfromhell",
        "simplemediawiki",
        "wsgiref"
    ],
  version = '0.11',
  description = 'Python library for accessing online data about Makerspaces, Fab Labs, Hackerspaces, TechShop...',
  author = 'Massimo Menichinelli',
  author_email = 'info@openp2pdesign.org',
  url = 'https://github.com/openp2pdesign/PyMakerspaces',
  download_url = 'https://github.com/openp2pdesign/PyMakerspaces/releases/tag/v0.1',
  keywords = ['FabLab', 'Makerspace', 'Hackerspace'],
  classifiers = ["Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",],
)