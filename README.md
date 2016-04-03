#OpenStreetMap Data Wrangling with MongoDB

This is project 3 of Udacity's Data Analyst Nanodegree.

##Openstreetmap Data for a Small Area in Central London

I started with london.osm, an XML file of size 67.7 MB containing [Openstreetmap](https://www.openstreetmap.org) data for a custom area in central London, obtained with [Overpass API](http://overpass-api.de/query_form.html). For this project, I chose to wrangle street name, postal code and phone number data using Python and MongoBD.

##Problems Encountered in the Map Data

I have summarized the auditing approachd and the problems detected in "Auditing of map data". In "Data tranformation" I present the methods used to clean and tidy the data in order to resolve a selection of the encountered problems.

At this stage, I worked only on the XML data downloaded from Openstreetmap. At the end of data transformation process, I produced a JSON file ready to be uploaded to MongoDB. All work with data in MongoDB is presented in "Data Overview".

###Auditing of map data

I audited street names, postal codes and phone numbers using Python scripts to analyse the XML data in london.osm. The objective was to spot inconsistencies and mistakes in data value or format.

For street names, I used ```audit_street.py```, a custom Python script based off of Udacity's code. For postal codes and phone numbers, I used code like ```audit_phone.py``` to print out all values and eyeball the data.

####1. Problems with street names

I examined the values associated with the XML tag "street" and detected several kinds of mistakes and inconsistencies in street name data. 

1. Abbreviations
2. Small caps

#####Abbreviation

#####Small caps

Auditing of street names: purpose, tools/scripts used, findings...
How many?

Abbreviations
- St.
- St
- Sq
- Rd

Small caps
lane, place, street, market, place

Other inconsistencies and mistakes
- Steet for Street

Unaddressed: Not street names

###2. Problems with postal codes
..

###3. Problems with phone numbers
Auditing of phone number: purpose, tools/scripts used, findings...

#How many numbers?

##Data tranformation


##Data Overview

###Importing into MongoDB

###Create database

mongod --dbpath /users/robertozanchi/Desktop/Udacity/DAND/P3/data/db


###Import into "london" collection within "maps" db

mongoimport --file /users/robertozanchi/Desktop/Udacity/DAND/P3/london.osm.json --db maps --collection london


2016-04-03T21:25:03.266+0200	connected to: localhost
2016-04-03T21:25:06.253+0200	[#######.................] maps.london	19.6 MB/63.8 MB (30.7%)
2016-04-03T21:25:09.255+0200	[##############..........] maps.london	39.3 MB/63.8 MB (61.6%)
2016-04-03T21:25:12.251+0200	[#######################.] maps.london	62.1 MB/63.8 MB (97.4%)
2016-04-03T21:25:12.647+0200	[########################] maps.london	63.8 MB/63.8 MB (100.0%)
2016-04-03T21:25:12.648+0200	imported 287928 documents


###Data

> db.london.count()
287928


##Additional Ideas

1. Incomplete post codes: completing post codes would require searching using the complete address of a place

Resources:

phonenumbers 7.2.8 | https://pypi.python.org/pypi/phonenumbers | 
sudo pip install git+git://github.com/daviddrysdale/python-phonenumbers.git