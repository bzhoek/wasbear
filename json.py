# for jython 2.1

from java.lang import System
print System.getProperty("java.version")

from com.google.gson import Gson

from com.google.gson import JsonParser
parser = JsonParser()
json = parser.parse("{'node':{'name':'node01'}}")
node = json.get('node')
