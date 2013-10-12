print "Processing %s" % sys.argv[0]
dict_data = open(sys.argv[0]).read()
dict = eval(dict_data)

nodeName = dict['node']['name']
node = AdminConfig.getid('/Node:%s/' % nodeName)

def createServer(param):
  serverName = param['node']['server']['name']
  server = AdminConfig.create('Server', node, [['name', serverName]])

def createDataSource(param, providerName):
  provider = AdminConfig.getid("/Node:%s/JDBCProvider/%s" % (nodeName, providerName))
  dataSourceName = param['name']
  print "Creating data source %s" % dataSourceName
  dataSource = AdminConfig.getid("/Node:%s/JDBCProvider:%s/DataSource:%s" % (nodeName, providerName, dataSourceName ))
  mapping = ['mapping',[['authDataAlias', param['j2c']], ['mappingConfigAlias', param['mapping']]]]
  attrs = [['name', dataSourceName], ['jndiName', param['jndiName']], mapping]
  dataSource = AdminConfig.create('DataSource', provider, attrs)

def createJdbcProvider(param):
  providerName = param['name']
  print "Creating JDBC Provider %s" % providerName
  provider = AdminConfig.getid("/Node:%s/JDBCProvider/%s" % (nodeName, providerName))
  attrs = [['name', param['name']],
    ['classpath', param['classpath']],
    ['implementationClassName', param['implementationClassName']],
    ['description', param['description']]]

  provider = AdminConfig.create('JDBCProvider', node, attrs)
  createDataSource(param['dataSource'], provider)

print dict['node']['name']

createJdbcProvider(dict['node']['jdbc'])
