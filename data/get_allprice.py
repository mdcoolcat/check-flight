#!/usr/bin/python
#Copyright 2012 DanielleMei

from os import getcwd
import httplib
import urllib, urllib2
import urlparse
import re
import pymongo
import datetime
import logging
import sys
from shutil import copyfileobj
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
    #content = ''
    try:
        page = urllib2.urlopen(req)
        content = page.read()
     #   copyfileobj(page, content)
    except urllib2.URLError, e:
        logger = logging.getLogger('get_price')
        logger.warning('URLError: ' + e.reason)
        print 'URLError: %s'% e.reason
        return None 
    except httplib.IncompleteRead, e:
        logger = logging.getLogger('get_price')
        logger.error('Unexpected exception: %s' % e)
        print 'Unexpected exception: %s' % e 
        return None 
    except Exception, e:
        logger = logging.getLogger('get_price')
        logger.error('Unexpected exception: %s' % e)
        print 'Unexpected exception: %s' % e 
        return None
    
    #return page.read().decode(page.headers.getparam('charset'))
    return content 

def extract_lowest(content):
    pattern = '<span id="lowestPrice">(\d+)</span>'
    match = re.findall(pattern, content)
    if not match:
        #f = open('price.html', 'wb')
        #f.write(content)
        #f.close()
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

def set_logger():
    logger = logging.getLogger('get_price')
    logging.basicConfig(filename='../Log/get_price.log',
            level=logging.DEBUG)
    hdlr = logging.FileHandler('../Log/get_price.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    return logger

def main():
    #set logger
    logger = set_logger()
#    logger.setLevel(logging.WARNING)

    site = 'http://www.expedia.com/Flights-search'
    dest = ['HKG', 'BJS']

    ## database
    conn = None
    try:
        conn = pymongo.Connection()
        db = conn.flight_db
        prices = db.prices
        # get all USA airport
        c = db.airports.find({
            'country' : 'USA'
            }, timeout=False)
        
        ## crawler
        trip_type = 'roundtrip'
        psg = {
                'children' : 0,
                'adults'   : 1,
                'seniors'  : 0
        }
        for d in dest:
        #d = dest[1]
            logger.info('Begin collecting price to %s' % d)
            c.rewind()
            for airport in c:
                depart = airport['code']
                query = construct_query(trip_type, depart, d, psg)
                content = get_page(site+'?'+query)
                if content is None: 
                    continue
                p = extract_lowest(content)
                if p < 0:
                    logger.warning('price of ' + airport['city'] + ' not found')    
                    continue

                prices.insert({
                        'date':datetime.datetime.utcnow(),
                        'dest':d,
                        'depart':depart,
                        'price': int(p) 
                }, safe=True)
        #conn.disconnect()
    except (pymongo.errors.OperationFailure, pymongo.errors.AutoReconnect), e: 
        logger.error('Mongo DB error: %s' % e)
        print e
    except Exception, e:
        logger.error('Unexpected exception: %s' % e)
        print 'Unexpected exception: %s' % e 
    finally:
        if conn is not None:
            conn.disconnect()
        sys.exit(1)

if __name__ == '__main__':
    main()
