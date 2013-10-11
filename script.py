print "Processing %s" % sys.argv[0]
dict_data = open(sys.argv[0]).read()
dict = eval(dict_data)

nodeName = dict['node']['name']
node = AdminConfig.getid('/Node:%s/' % nodeName)

serverName = dict['node']['server']['name']
server = AdminConfig.create('Server', node, [['name', serverName]])

print dict['node']['name']