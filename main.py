#!/usr/bin/python
#Copyright 2012 DanielleMei

import sys
import re
import urllib2, cookielib
import codecs



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
    
    return page.read().decode(page.headers.getparam('charset'))

def extract_lowest(content):
    pattern = '<span id="lowestPrice">(\d+)</span>'
    match = re.findall(pattern, content)
    if not match:
        print 'error: price not found...'
        exit(1)
    return match[0]


def main():
    site = 'http://www.expedia.com/Flights'
    trip_type = 'RoundTrip'
    depart = 'Boston, MA (BOS-Logan Intl.)'
    from_date = '8/10/2012'
    dest = 'New York, NY, United States (NYC - All Airports)'
    to_date = '8/17/2012'

    url = 'http://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from%3ANew+York%2C+NY%2C+United+States+%28NYC+-+All+Airports%29%2Cto%3ABoston%2C+MA%2C+United+States+%28BOS+-+All+Airports%29%2Cdeparture%3A08%2F10%2F2012TANYT&leg2=from%3ABoston%2C+MA%2C+United+States+%28BOS+-+All+Airports%29%2Cto%3ANew+York%2C+NY%2C+United+States+%28NYC+-+All+Airports%29%2Cdeparture%3A08%2F17%2F2012TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy%2Cnopenalty%3AN%2Csortby%3Aprice&mode=search'
    content = get_page(url)
    f = open('r.html', 'wb')
    f.write(content)
    f.close()
    
    print extract_lowest(content)


if __name__ == '__main__':
    main()
