print "Processing %s" % sys.argv[0]
dict_data = open(sys.argv[0]).read()
dict = eval(dict_data)

separator = java.lang.System.getProperty("line.separator")

nodeName = dict['node']['name']
node = AdminConfig.getid('/Node:%s/' % nodeName)


def showAttribute(object, name):
  return AdminConfig.showAttribute(object, name)


def createServer(param):
  serverName = param['node']['server']['name']
  server = AdminConfig.create('Server', node, [['name', serverName]])


def createDataSource(param, providerName):
  provider = AdminConfig.getid("/Node:%s/JDBCProvider/%s" % (nodeName, providerName))
  dataSourceName = param['name']
  print "Creating data source %s" % dataSourceName
  dataSource = AdminConfig.getid("/Node:%s/JDBCProvider:%s/DataSource:%s" % (nodeName, providerName, dataSourceName ))
  mapping = ['mapping', [['authDataAlias', param['j2c']], ['mappingConfigAlias', param['mapping']]]]
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


def createVariable(param):
  variables = AdminConfig.list("VariableSubstitutionEntry", node).split(separator)
  for variable in variables:
    if param['name'] == showAttribute(variable, "symbolicName"):
      AdminConfig.modify(variable, [['value', param['value']]])
      return


print dict['node']['name']

# createJdbcProvider(dict['node']['jdbc'])
createVariable(dict['node']['variable'])
AdminConfig.save()