#!/usr/bin/python
# Copyright 2012 DanielleMei

import sys
import re
import pymongo

"""Extract all international aiports from expedia website, store in mongodb
   as {'city', 'country', 'code'}

Here's what the html looks like in the html files:
....
<td class="city sorted">Badajoz</td>
<td class="country">Spain</td>
<td class="code"><a href="javascript:gotoFlight('BJZ');">BJZ</a></td>
....


"""

def get_airports(cities):
    """
    query from configure.py. print out the result and return list
    """
    ## Database connection, db, collection
    conn = pymongo.Connection()
    db=conn.flight_db
    ap = db.airports

    airport_list = []
    for city in cities:
        c = ap.find({
            'city':{'$regex':'^'+city, '$options':'i'}
            })
        for info in c:
            airport_list.append(info['city'] + ': ' + info['code'])
            print '%s - %s' % (info['city'], info['code'])
    conn.disconnect()

    return airport_list

def extract_airports(filename, store):
  """
   read the file, extract airport info from the html with regex
   store each aiport info in mongodb as document {'city', 'country', 'code'}
  """
  print filename
  f = open(filename, 'r')
  text = f.read()
  f.close()
  
  if store:
      ## Database connection, db, collection
      conn = pymongo.Connection()
      db=conn.flight_db
      ap = db.airports

  airport_list = []
  
  ## extract city,country,airport code
  #match = re.findall(r'<td\s*class=\"city sorted\">(.*?)<\/td>\s+<td\s*class=\"country\">(\w+?)</td>\s+<td\s*class=\"code\"><a\s*href=.+\">(\w+?)</a></td>\s+', text)
  match = re.findall(r'<td\s*class=\"city sorted\">(.*?)<\/td>\s+<td\s*class=\"country\">(\w+?)</td>\s+<td\s*class=\"code\"><a\s*href=.+\">(\w+?)</a><span\s*style=.*', text)
  if not match:
      print 'airport:rank not found...'
      exit(1)
  for tuples in match:
      if store:
          ap.insert({
                  'city':tuples[0],
                  'country':tuples[1],
                  'code':tuples[2]
          })
      airport_list.append(tuples[0] + ', ' + tuples[1] + ' - ' + tuples[2])
  if store:
    conn.disconnect()
  return airport_list


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [-d] file [file ...] [-w]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  store_db = False
  write_file = False
  if args[0] == '-d':
      store_db = True
      del args[0]
  if args[0] == '-w':
      write_file = True
      del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  for filename in args:
      airport_list = extract_airports(filename, store_db)
      if write_file: 
        sum_file = filename + '--summaryfile'
        f = open(sum_file, 'w')
      for s in airport_list:
          if write_file: 
              f.write(s + '\n')
          else:
              print s
      if write_file:   
          f.close()


if __name__ == '__main__':
  main()
