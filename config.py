try:
    import json
except ImportError:
    import simplejson as json

json_data = open('config.json')
data = json.load(json_data)
dict_data = open('config.dict', 'w')
dict_data.write(str(data))

# {u'node': {u'name': u'precise64Node01', u'server': {u'name': u'server2'}}}
# atad = eval("{u'node': {u'name': u'precise64Node01', u'server': {u'name': u'server2'}}}")
