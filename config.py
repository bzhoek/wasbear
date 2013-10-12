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
AdminConfig.create('StringNameSpaceBinding', server, [['name', 'binding1'], ['nameInNameSpace', 'myBindings/myString'],
  ['stringToBind', "This is the String value that gets bound"]])
binding = AdminConfig.getid('/Node:%s/Server:%s/StringNameSpaceBinding:%s' % (nodeName, serverName, "binding1"))

# jdbcProvider
providerName = 'DB2JDBCProvider'
provider = AdminConfig.getid("/Node:%s/JDBCProvider/%s" % (nodeName, providerName))

# jaas
cellName = "precise64Node01Cell"
security = AdminConfig.getid("/Cell:%s/Security:/" % cellName)
authAlias = "precise64Node01/db2inst1"
AdminConfig.create('JAASAuthData', security,
  [['alias', authAlias], ['userId', "db2inst1"], ['password', "p@ssw0rd"], ['description', '']])

# install
print AdminApp.taskInfo('/vagrant/ics-ear-13.4.0-SNAPSHOT-nl.ear', 'MapResEnvRefToRes')
AdminApp.install('/vagrant/iwa-usermanagement-server-ear-13.4.0.1-SNAPSHOT.ear', [
  '-MapResRefToEJB', [[
    'iwa-usermanagement-server',
    '',
    'iwa-usermanagement-server.war,WEB-INF/web.xml',
    'jdbc/ics/userdataDB',
    'javax.sql.DataSource',
    'jdbc/ics/userdataDB',
    '',
    '',
    '']],
  '-MapWebModToVH', [['.*', '.*', 'default_host']]])