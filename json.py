# for jython 2.1

from java.lang import System
print System.getProperty("java.version")

# JsonParser
from com.google.gson import JsonParser
parser = JsonParser()

# read from file
from java.io import FileReader
reader = FileReader("server.json")
json = parser.parse(reader)
json.get('node').isJsonArray()

json = parser.parse("{'node':{'name':'node01'}}")
node = json.get('node')

