#!/usr/bin/python
#Copyright 2012 DanielleMei

from os import getcwd
import urllib, urllib2
import urlparse
import re
import pymongo
import datetime
import logging
import sys, time
from daemon import Daemon
#import codecs
#path.append(getcwd() + '../Config')

class MyDaemon(Daemon):
    def run(self):
        the_main()
        exit(0)


def get_page(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
            'Referer': 'http://www.expedia.com/Flights'
    }
    req = urllib2.Request(
            url = url,
            headers = headers
    )
    try:
        page = urllib2.urlopen(req)
    except urllib2.URLError, e:
        logger = logging.getLogger('get_price')
        logger.warn('URLError: ' + e.reason)
        print 'URLError: %s'% e.reason
        return None 
    except Exception, e:
        logger = logging.getLogger('get_price')
        logger.warn('Unexpected exception: ' + e)
        print 'Unexpected exception: %s' % e 
        return None
    
    #return page.read().decode(page.headers.getparam('charset'))
    return page.read()

def extract_lowest(content):
    pattern = '<span id="lowestPrice">(\d+)</span>'
    match = re.findall(pattern, content)
    if not match:
        print 'error: price not found...'
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

def the_main():
    #set logger
    logger = logging.getLogger('get_price')
    logging.basicConfig(filename='../Log/get_price.log',
            level=logging.WARNING)
    time.sleep(5)
    hdlr = logging.FileHandler('../Log/get_price.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
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
        for airport in c:
            depart = airport['code']
            print depart
            query = construct_query(trip_type, depart, dest[0], psg)
            content = get_page(site+'?'+query)
            if content is None: 
                continue
            p = extract_lowest(content)
            if p < 0:
                logger.warn('price of ' + airport['city'] + ' not found')    
                continue

            prices.insert({
                    'date':datetime.datetime.utcnow(),
                    'dest':dest[0],
                    'depart':depart,
                    'price': int(p) 
            }, safe=True)
        conn.disconnect()
    except (pymongo.errors.OperationFailure, pymongo.errors.AutoReconnect), e: 
        logger.error(e)
        print e
        if conn is not None:
            conn.disconnect()
        sys.exit(1)

if __name__ == '__main__':
    #main()
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
