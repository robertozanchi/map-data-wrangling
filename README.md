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

Among the values that didn't match the list, I detected different types of mistakes and inconsistencies:

1. Abbreviation of street names
2. Small caps
3. Typos
4. Mistakes

#####1. Abbreviation of street names

An inconsistency problem in data format. A small number of values included abbreviations for ```Road```, ```Street``` and ```Square``` instead of their full form. These values were: ```Rd```, ```St```, ```St.``` and ```Sq```.

#####2. Small caps

Another inconsistency problem in data format. I found instances of ```lane```, ```place```, ```street``` and ```market``` instead of their standard capitalized versions.

#####3. Typos

Certain street names had a spelling mistake in how they were written. A case I found was ```Steet``` where the user probably meant to input ```Street```, and ```Picadilly``` for ```Piccadily```.

#####4. Mistakes

Several values were found that were not street names. For example ```Chelsea```, ```Lambeth``` and ```Mayfair```, which are names of neighborhoods, or ```5A``` which appears to be a house number.

####2. Problems with post codes

Printing out post codes highlighted a frequent problem related to partial post code information. A complete post code in London has two parts and looks like this: ```NW1 2BU```. Many values only included the first half of the postcode, e.g. ```NW1```.

The first half of a post code corresponds to a larger area of the city than the full post code. Therefore, availability of halves of post codes leads to a problem of lack of complete detail more than wrong location.

####3. Problems with phone numbers

Simply by printing out phone number values, I detected a number types of mistakes and inconsistencies:

1. Missing phone numbers
2. Inconsistent formatting
3. Not a phone number  

#####1. Missing phone numbers

The list of all phone numbers available in the data is relatively short. This points at a case of missing phone number information scarsity in the data.

#####2. Inconsistent formatting

Looking at the phone numbers that were printed out shows a number of inconsistent use of conventions. For example: 

```
+44 20 74051992
+44-20-79352361
+44 20 7620 328
+442073704988
0207 850 0500
+44 (0)20 74025077
442074018080
```

The formatting problems in this small sample include:
- Mixed use of national and international formats with country code ```+44```
- Use of ```0``` before the London city prefix (20) when the country code is missing
- Uneven use of brackets ```( )``` and dashes ```-```
- Uneven spacing between digits

#####3. Not a phone number

I found one instance of a string like ```+44 +44 20 73001000.``` where the country code was entered twice and which ended with a full stop. My guess is that the user meant to input ```+44 20 73001000``` instead.

##Data transformation

I decided to address a selection of the problems discussed above by using ```transform.py```, a Python script, to clean and tidy the data. The script resolved the following data issues:

- Abbreviation of street names
- Small caps in street names
- Typos in street names
- Replacement of ```+44 +44 20 73001000.``` with presumed correct number

The method used to solve these problems is string substitution of problematic values with the correct values.

To solve all the problems related to street names, I used a list of tuples containing values to be replaced and correct values:
```
STREET_CORRECT = [
    ("lane", "Lane"),
    ("market", "Market"),
    ("Picadilly", "Piccadilly"),
    ("place", "Place"),
    ("Rd", "Road"),
    ("St ", "Street"),
    ("St.", "Street"),
    ("Steet", "Street"),
    ("street", "Street"),
    ("Street.", "Street"),
    ("Sq", "Square"),
    ("turnstile", "Turnstile")
]
```

To replace the incorrect phone number value, I used the ```update_phone_number()``` function in ```transform.py```.

Taking ```london.osm``` as input, ```transform.py``` corrects these problems during the conversion of XML values into JSON. The resulting "clean" output file ```london.osm.json```, of size 66.9 MB, is ready to be uploaded to MongoDB.

##Data Overview

###1. Get MongoDB up and running



####1. Install MongoDB

As a first thing, I installed MongoDB on my Mac using [Homebrew](http://brew.sh/) and the official [MongoDB installation tutorial](https://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/).

####2. Create MongoDB database

Before importing the clean data file, I had created a local MongoDB database using the following command:

```
mongod --dbpath /users/robertozanchi/Desktop/Udacity/DAND/P3/data/db
```

####3. Import data file into MongoDB

I imported the JSON file into a ```london``` collection within a newly created ```maps``` database, using the command:

```
mongoimport --file /users/robertozanchi/Desktop/Udacity/DAND/P3/london.osm.json --db maps --collection london

2016-04-03T21:25:03.266+0200	connected to: localhost
2016-04-03T21:25:06.253+0200	[#######.................] maps.london	19.6 MB/63.8 MB (30.7%)
2016-04-03T21:25:09.255+0200	[##############..........] maps.london	39.3 MB/63.8 MB (61.6%)
2016-04-03T21:25:12.251+0200	[#######################.] maps.london	62.1 MB/63.8 MB (97.4%)
2016-04-03T21:25:12.647+0200	[########################] maps.london	63.8 MB/63.8 MB (100.0%)
2016-04-03T21:25:12.648+0200	imported 287928 documents
```

###2. Data analysis

Within MongoDB I performed analysis of data using the following commands.

Number of documents
```
> db.london.count()
287928
```

Number of nodes
```
> db.london.find({type: "node"}).count()
242133
```

Number of ways
```
> db.london.find({type: "way"}).count()
45795
```

##Additional Ideas

1. Incomplete post codes: completing post codes would require searching using the complete address of a place

Resources:

phonenumbers 7.2.8 | https://pypi.python.org/pypi/phonenumbers | 
sudo pip install git+git://github.com/daviddrysdale/python-phonenumbers.git