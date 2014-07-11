# Converts a JSON file to a serialized dictionary, that can be deserialized by an Jython 2.1
import sys

try:
  import json
except ImportError:
  import simplejson as json

infile = (len(sys.argv) > 1) and sys.argv[1] or "config.json"
outfile = (len(sys.argv) > 2) and sys.argv[2] or "config.dict"

json_data = open(infile)
data = json.load(json_data)
dict_data = open(outfile, 'w')
dict_data.write(str(data))

print "Converted '%s' to '%s'" % (infile, outfile)