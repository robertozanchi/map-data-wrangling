#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xml.etree.cElementTree as ET
import re
import codecs
import json
import phonenumbers

CREATED = ["version", "changeset", "timestamp", "user", "uid"]

STREET_EXPECTED = ["Acre", "Approach", "Arch", "Avenue", "Bridge", "Circle", "Circus", "Close", "Corner",
            "Court", "Crescent", "Drive", "East", "Embankment", "Estate", "Garden", "Gardens", "Gate", "Grove",
            "Hill", "Lane", "Market", "Mews", "North", "Place", "Road", "Row", "South", "Square", "Station",
            "Street", "Terrace", "Walk", "Way", "West", "Wharf", "Yard"]

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


def is_address(tag_key):
    return tag_key.startswith('addr:')


def is_address_street(tag_key):
    return tag_key == 'addr:street'


def is_address_detail(tag_key):
    return is_address(tag_key) and len(tag_key.split(':')) == 3


def has_colon(tag_key):
    return ':' in tag_key


def is_street_good(street_name, expected):
    for pattern in expected:
        if re.search(pattern, street_name):
            return True
    return False


def update_street_name(name, mapping):
    """
    Change street name according to standard rules in STREET_CORRECT list
    """
    for bad, good in mapping:
        name = re.sub(bad, good, name)
    name = name.strip()
    return name


def is_contact(tag_key):
    return tag_key.startswith('contact:')


def is_contact_phone(tag_key):
    return tag_key == 'contact:phone'


def update_phone_number(tag_val):
    if tag_val == '+44 +44 20 73001000.':
        return '+44 20 73001000'
    else:
        corrected_number = phonenumbers.format_number(phonenumbers.parse(tag_val, 'GB'), phonenumbers.PhoneNumberFormat.NATIONAL)
    # x = phonenumbers.parse(tag_val, "GB")
    # node['phone'] = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return corrected_number


def add_tag_info(node, tag_key, tag_val):
    """
    Add tag key and value, special treatment for addresses
    """
    # Add address information to node
    if is_address(tag_key):
        address_part = tag_key.split(':')[1] # Takes sub (e.g. "street") element of tag key
        if 'address' not in node:
            node['address'] = {}
        if is_address_street(tag_key) and not is_street_good(tag_val, STREET_EXPECTED):
            tag_val = update_street_name(tag_val, STREET_CORRECT) # Correct street name
        node['address'][address_part] = tag_val
    
    #New code to tranform phone numbers
    if is_contact(tag_key):
        if is_contact_phone(tag_key):
            # print tag_val # Prints phone number            
            node['phone'] = update_phone_number(tag_val)
    #End new code
    
    elif has_colon(tag_key):
        pass
    elif tag_key == 'type':
        # We already have "type", it's either "node" or "way".
        # Let's rename "type" to "type_tag" so we don't confuse the two.
        node["type_tag"] = tag_val
    else:
        node[tag_key] = tag_val
    
    return node


def add_attr_info(node, attr_key, attr_val):
    """
    Reshape node
    """
    if attr_key == 'lat':
        node['pos'] = [float(attr_val)] + node.get('pos', [])
    elif attr_key == 'lon':
        node['pos'] = node.get('pos', []) + [float(attr_val)]
    elif attr_key in CREATED:
        created = node.get('created', {})
        created[attr_key] = attr_val
        node['created'] = created
    else:
        node[attr_key] = attr_val
    return node


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        node['type'] = element.tag
        for k, v in element.items():
            node = add_attr_info(node, k, v)
        for tag in element.iter("tag"):
            # Adds tag info with corrected address and phone to the node using add_tag_info function
            node = add_tag_info(node, tag.attrib['k'], tag.attrib['v'])
        for nd in element.iter('nd'):
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'] += [nd.attrib['ref']]
        return node
    else:
        return None


def process_map(file_in, pretty=False):
    """
    Process and rewrite OSM file data to structured JSON
    """
    file_out = "{0}.json".format(file_in)
    with codecs.open(file_out, "w", encoding='utf-8') as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                if pretty:
                    json.dump(el, fo, ensure_ascii=False, indent=2)
                    fo.write("\n")
                else:
                    json.dump(el, fo, ensure_ascii=False)
                    fo.write("\n")


def process():
    process_map('london.osm', False)


if __name__ == "__main__":
    process()