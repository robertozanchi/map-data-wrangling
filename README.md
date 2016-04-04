#OpenStreetMap Data Wrangling with MongoDB

This is project 3 of Udacity's Data Analyst Nanodegree.

##Openstreetmap Data for Central London

I started with london.osm, a 67.7 MB XML file containing [Openstreetmap](https://www.openstreetmap.org) data for a custom area in central London, obtained with [Overpass API](http://overpass-api.de/query_form.html). I chose to wrangle street name, postal code and phone number data using Python and MongoBD.

##Problems Encountered in the Map Data

In "Audit of map data" I summarize the auditing approach and the problems detected. In "Data tranformation" I present the methods used to clean and tidy the data in order to resolve a selection of the problems encoutered.

At this stage I worked only on the XML data downloaded from Openstreetmap. At the end of data transformation process, I produced a JSON file ready to be uploaded to MongoDB. All work with data in MongoDB is presented in "Data Overview".

###Audit of map data

The objective of auditing was to spot inconsistencies and mistakes of value or format in the data. I audited street names, postal codes and phone numbers in london.osm by analysing the XML data with Python scripts. 

To audit street names, I used ```audit_street.py```, a custom Python script based off of Udacity's code. The script prints all values associated with the "street" tag that don't match those in a list of expected values.

To audit postal code and phone number data, I used code like ```audit_phone.py``` to print out all values. Post codes and phone numbers are short strings, and some problems can be spotted simply by eyeballing the data.

####1. Problems with street names

To find mistakes more easily, I filtered out correct street names using the list of expected values below. I ran ```audit_street.py``` several times, each time finding new names to add to the list.

```
expected = ["Acre", "Approach", "Arch", "Avenue", "Bridge", "Circle", "Circus", "Close", "Corner", "Court",
            "Crescent", "Drive", "East", "Embankment", "Estate", "Garden", "Gardens", "Gate", "Grove", "Hill",
            "Lane", "Market", "Mews", "North", "Place", "Road", "Row", "South", "Square", "Station", "Street",
            "Terrace", "Walk", "Way", "West", "Wharf", "Yard"]
```

Among the values that dodn't match the list, I detected different types of mistakes and inconsistencies:

1. Abbreviation of street names
2. Small caps
3. Typos
4. Other mistakes

#####1. Abbreviation of street names

An inconsistency problem in data format. A small number of values included abbreviations for "Road", "Street" and "Square" instead of their full form. These values were: "Rd", "St", "St." and "Sq".

#####2. Small caps

Another inconsistency problem in data format. I found instances of ```lane```, ```place```, ```street``` and ```market``` instead of their standard capitalized version.

#####3. Typos

Certain street names had a spelling mistake in how they were written. A case I found was ```Steet``` where the user probably meant to input ```Street```.

#####4. Other mistakes

Several values were found that were not street names. For example ```Chelsea```, ```Lambeth``` and ```Mayfair```, which are name of neighborhoods, or ```5A``` which appears to be a house number.

###2. Problems with postal codes

Printing out post codes helped to highlight some problems in the data. The main problem detected was that of 

###3. Problems with phone numbers
Auditing of phone number: purpose, tools/scripts used, findings...

####Missing phone numbers
- How many numbers

####Inconsistent formatting 
- National vs internatial
- 0 before city prefix
- parenthesis and dashes
- Spacing between digits

####Not a number
- Found only one

##Data tranformation


##Data Overview

###Importing into MongoDB

###Create database
```
mongod --dbpath /users/robertozanchi/Desktop/Udacity/DAND/P3/data/db
```

```
###Import into "london" collection within "maps" db
```
```
mongoimport --file /users/robertozanchi/Desktop/Udacity/DAND/P3/london.osm.json --db maps --collection london
```

```
2016-04-03T21:25:03.266+0200	connected to: localhost
2016-04-03T21:25:06.253+0200	[#######.................] maps.london	19.6 MB/63.8 MB (30.7%)
2016-04-03T21:25:09.255+0200	[##############..........] maps.london	39.3 MB/63.8 MB (61.6%)
2016-04-03T21:25:12.251+0200	[#######################.] maps.london	62.1 MB/63.8 MB (97.4%)
2016-04-03T21:25:12.647+0200	[########################] maps.london	63.8 MB/63.8 MB (100.0%)
2016-04-03T21:25:12.648+0200	imported 287928 documents
```

###Data

> db.london.count()
287928


##Additional Ideas

1. Incomplete post codes: completing post codes would require searching using the complete address of a place

Resources:

phonenumbers 7.2.8 | https://pypi.python.org/pypi/phonenumbers | 
sudo pip install git+git://github.com/daviddrysdale/python-phonenumbers.git