import argparse
from sys import path
from os import getcwd
path.append(getcwd() + '/Config')
path.append(getcwd() + '/Data')
import config
from get_airport import get_airports

def parse_args():
    parser = argparse.ArgumentParser(
            description='Configure flight details')
    
    ## trip type, round-trip / one-way
    parser.add_argument(
            '--oneway', action='store_false', dest='trip_type', 
            default=True, help='Search for one-way flight')
    parser.add_argument(
            '--rr', action='store_true', dest='trip_type', 
            default=False, help='Search for round-trip flight')
    ## flight details
    parser.add_argument('--from-ap', action='store', dest='depart', 
            help='Specify the departure airport')
    parser.add_argument('--from-date', action='store', dest='from_d', 
            help='Specify the departure date, mm/dd/yyyy')
    parser.add_argument('--to-ap', action='store', dest='dest', 
            help='Specify the destination airport')
    parser.add_argument('--to-date', action='store', dest='to', 
            help='Specify the return date, mm/dd/yyyy')

    ## other options
    parser.add_argument('--default', action='store_true', dest='psg', default=True, help='Use default settings on the number and type of passenger')
    parser.add_argument('--ad', action='store', dest='adult', 
            type=int, default=1, help='Number of adults')
    parser.add_argument('--ch', action='store', dest='child', 
            type=int, default=1, help='Number of children')
    parser.add_argument('--se', action='store', dest='senior', 
            type=int, default=1, help='Number of seniors')

    ## version
    parser.add_argument(
            '--version', action='version', version='check flight 1.0')
    ## list airports
    parser.add_argument(
            '--list', dest='list_ap', nargs = '+',
            help='List airport code(s) by city(cities). Use \ before space')

    return parser.parse_args()

def list_ap(cities):
    get_airports(cities)

def main():
    args = parse_args()
    if args.list_ap is not None:
        list_ap(args.list_ap)
        exit(0)

    fields = {}
    
    fields['trip_type'] = args.trip_type
    fields['psg'] = args.psg

    if args.depart is not None:
        fields['depart'] = args.depart
    if args.from_d is not None:
        fields['from_date'] = args.from_d
    if args.dest is not None:
        fields['dest'] = args.dest
    if args.to is not None:
        fields['to_date'] = args.to
    
    if fields['psg']:
        print 'default...'

    config.update_conf(fields)


if __name__ == '__main__':
    main()
