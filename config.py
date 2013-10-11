nodeName = "precise64Node01"
node = AdminConfig.getid('/Node:%s/' % nodeName)

# createServer
serverName = "server2"
server = AdminConfig.create('Server', node, [['name', serverName]])

# removeServer
server = AdminConfig.getid('/Node:%s/Server:%s' % (nodeName, serverName))
AdminConfig.remove(server)

# resourceEnvironmentProvider
rep = AdminConfig.create('ResourceEnvironmentProvider', server, [['name', serverName]])
rep = AdminConfig.getid('/Node:%s/Server:%s/ResourceEnvironmentProvider:%s' % (nodeName, serverName, serverName))

# stringNameSpaceBinding
AdminConfig.create('StringNameSpaceBinding', server, [['name', 'binding1'], ['nameInNameSpace', 'myBindings/myString'], ['stringToBind', "This is the String value that gets bound"]])
binding = AdminConfig.getid('/Node:%s/Server:%s/StringNameSpaceBinding:%s' % (nodeName, serverName, "binding1"))