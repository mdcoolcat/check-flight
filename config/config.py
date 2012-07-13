#!/usr/bin/python
#Copyright 2012 DanielleMei

import ConfigParser

conf = ConfigParser.ConfigParser()
flight_legs = None
passengers = None
optionals = None
site = None 
depart = None
dest = None
from_date = None
to_date = None

def section_map(section):
    d = {}
    options = conf.options(section)
    for opt in options:
        try:
            d[opt] = conf.get(section, opt)
            if d[opt] == -1:
                print ('skip: %s' % opt)
        except:
            print("exception on %s!" % opt)
            d[opt] = None
    return d


#def main():
def get_conf():
    conf.read('./config/flight.cfg')
    sections = conf.sections()
    flight_legs = section_map(sections[0])
    psg = section_map(sections[1])
    #optionals = section_map(sections[2])
    site = section_map(sections[2])['site']
    #return {'legs':flight_legs, 
     #       'psg' : psg,
     #       'site' : site
     #       }

    trip_types = flight_legs['trip_type']
    leg1 = {
            'from'      : flight_legs['depart'], 
            'to'        : flight_legs['dest'], 
            'departure' : flight_legs['from_date']
    }
    leg2 = {
            'from'      : flight_legs['dest'], 
            'to'        : flight_legs['depart'], 
            'departure' : flight_legs['to_date']
    }
    #print leg1['from']
    #print type(leg1['from'])
    passengers = {
            'children' : int(psg['children']), 
            'adults'   : int(psg['adults']),
            'seniors'  : int(psg['seniors'])
    }
    return {
            'site' : site,
            'trip' : flight_legs['trip_type'],
            'leg1': leg1,
            'leg2': leg2,
            'passengers': passengers 
            }


if __name__ == '__main__':
    main()
