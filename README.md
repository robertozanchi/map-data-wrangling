#OpenStreetMap Data Wrangling with MongoDB

##1. Problems Encountered in the Map

###Auditing of map data
I checked street names, postal codes and phone numbers.

For street names, I used audit_street.py, a custom script based off of Udacity's code. 
For postal codes and numbers I simply printed the values out to spot inconsistencies by eyeballing the data.

####1. Problems with street names

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


##2. Data Overview

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


##3. Additional Ideas

1. Incomplete post codes: completing post codes would require searching using the complete address of a place

Resources:

phonenumbers 7.2.8 | https://pypi.python.org/pypi/phonenumbers | 
sudo pip install git+git://github.com/daviddrysdale/python-phonenumbers.git