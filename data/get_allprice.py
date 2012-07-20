#!/usr/bin/python
#Copyright 2012 DanielleMei

from sys import path
from os import getcwd
import urllib, urllib2
import urlparse
import re
import pymongo
import datetime
#import codecs
#path.append(getcwd() + '../Config')


def get_page(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
            'Referer': 'http://www.expedia.com/Flights'
    }
    req = urllib2.Request(
            url = url,
            headers = headers
    )
    page = urllib2.urlopen(req)
    
    #return page.read().decode(page.headers.getparam('charset'))
    return page.read()

def extract_lowest(content):
    pattern = '<span id="lowestPrice">(\d+)</span>'
    match = re.findall(pattern, content)
    if not match:
        print 'error: price not found...'
        f = open('price.html', 'wb')
        f.write(content)
        f.close()
        return -1
    return match[0]

def inside_format(d):
    pairs = []
    for key, value in d.items():
        new_pair = '%s:%s' % (key, value) 
        pairs.append(new_pair)

    return ','.join(pairs)

def construct_query(trip, depart, dest, psg):
    #depart flight
    leg1_details = {
            'from':depart,
            'to':dest,
            'departure':'12/24/2012TANYT'
    }
    leg1 = inside_format(leg1_details)

    #return flight
    leg2_details = {
            'from':dest,
            'to':depart,
            'departure':'1/20/2013TANYT'
    }
    leg2 = inside_format(leg2_details)

    #passengers
    p = inside_format(psg)

    query = urllib.urlencode({
        'trip' : trip,
        'leg1' : leg1,
        'leg2' : leg2,
        'passengers' : p,
        'mode' : 'search'
    })
    return query

def main():
    site = 'http://www.expedia.com/Flights-search'
    dest = ['HKG', 'BJS']

    ## database
    conn = pymongo.Connection()
    db = conn.flight_db
    prices = db.prices
    # get all USA airport
    c = db.airports.find({
        'country' : 'USA'
        })
    
    ## crawler
    trip_type = 'roundtrip'
    psg = {
            'children' : 0,
            'adults'   : 1,
            'seniors'  : 0
    }
    for airport in c:
        depart = airport['code']
        print depart
        query = construct_query(trip_type, depart, dest[0], psg)
        content = get_page(site+'?'+query)
        
        prices.insert({
                'date':datetime.datetime.utcnow(),
                'dest':dest[0],
                'depart':depart,
                'price': extract_lowest(content)
        }, safe=True)
    
    conn.disconnect()

if __name__ == '__main__':
    main()
