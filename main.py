#!/usr/bin/python
#Copyright 2012 DanielleMei

from os import getcwd
import urllib, urllib2
import urlparse
import re
import sys
#import codecs
sys.path.append(getcwd() + '/Config')

import config

def get_page(url):
    print '........'
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
        sys.exit(1)
    return match[0]

def inside_format(d):
    pairs = []
    for key, value in d.items():
        new_pair = '%s:%s' % (key, value) 
        pairs.append(new_pair)

    return ','.join(pairs)

def construct_query(cfg):
    trip_type = cfg['trip']
    
    #depart flight
    leg1_details = cfg['leg1']
    #set global variable for main function usage
    config.from_date = leg1_details['departure']
    config.depart = leg1_details['from']
    config.dest = leg1_details['to']
    #format date for expedia's url
    leg1_details['departure'] += 'TANYT' 
    leg1 = inside_format(leg1_details)

    #return flight
    leg2_details = cfg['leg2']
    config.to_date = leg2_details['departure']
    leg2_details['departure'] += 'TANYT' 
    leg2 = inside_format(leg2_details)

    #passengers
    p = inside_format(cfg['passengers'])
    #print p
    query = urllib.urlencode({
        'trip' : trip_type,
        'leg1' : leg1,
        'leg2' : leg2,
        'passengers' : p,
        'mode' : 'search'
    })
    return query

def main():
    #Option mappings from config file
    cfg = config.get_conf()
    site = cfg['site']
    query = construct_query(cfg)

    print '........Searching for flights........'
    print ('%s -- %s' % (config.depart, config.dest))
    print ('%s -- %s' % (config.from_date, config.to_date))

    content = get_page(site+'?'+query)
    f = open('r.html', 'wb')
    f.write(content)
    f.close()
    
    print extract_lowest(content)


if __name__ == '__main__':
    main()
