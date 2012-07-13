#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Here's what the html looks like in the baby.html files:
....
<td class="city sorted">Badajoz</td>
<td class="country">Spain</td>
<td class="code"><a href="javascript:gotoFlight('BJZ');">BJZ</a></td>

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_airports(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  f = open(filename, 'r')
  text = f.read()
  f.close()

  airport_list = []
  
  ## extract city,country,airport code
  match = re.findall(r'<td\s*class=\"city sorted\">(.*?)<\/td>\s+<td\s*class=\"country\">(\w+?)</td>\s+<td\s*class=\"code\"><a\s*href=.+\">(\w+?)</a></td>\s+', text)
  if not match:
      print 'airport:rank not found...'
      exit(1)
  print len(match)
  for tuples in match:
  #    print ('***%s\n%s\n%s\n') % (tuples[0],tuples[1], tuples[2])
      airport_list.append(tuples[0] + ', ' + tuples[1] + ' - ' + tuples[2])
  return airport_list


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  for filename in args:
      airport_list = extract_airports(filename)
      
      if summary:   
          sum_file = filename + '--summaryfile'
          f = open(sum_file, 'w')
      for s in airport_list:
          if summary: 
              f.write(s + '\n')
          else:
              print s
      if summary:   
          f.close()


if __name__ == '__main__':
  main()
