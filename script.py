print "Processing %s" % sys.argv[0]
dict_data = open(sys.argv[0]).read()
dict = eval(dict_data)

separator = java.lang.System.getProperty("line.separator")
nodeName = dict['node']['name']
node = AdminConfig.getid('/Node:%s/' % nodeName)


def printTypeName(type, param):
  print "Creating %s: %s" % (type, param['name'])


def showAttribute(object, name):
  return AdminConfig.showAttribute(object, name)


def createServer(param):
  printTypeName('server', param)
  serverName = param['node']['server']['name']
  server = AdminConfig.create('Server', node, [['name', serverName]])


def createDataSource(param, provider):
  printTypeName('data source', param)
  providerName = showAttribute(provider, 'name')
  dataSourceName = param['name']
  dataSource = AdminConfig.getid("/Node:%s/JDBCProvider:%s/DataSource:%s" % (nodeName, providerName, dataSourceName ))
  mapping = ['mapping', [['authDataAlias', param['j2c']], ['mappingConfigAlias', param['mapping']]]]
  attrs = [['name', dataSourceName], ['jndiName', param['jndiName']], mapping]
  dataSource = AdminConfig.create('DataSource', provider, attrs)
  propertySet = AdminConfig.create('J2EEResourcePropertySet', dataSource, [])
  AdminConfig.create('J2EEResourceProperty', propertySet, [['name', 'driverType'], ['type', 'java.lang.Integer'],
    ['value', param['driverType']]])
  AdminConfig.create('J2EEResourceProperty', propertySet, [['name', 'databaseName'], ['type', 'java.lang.String'],
    ['value', param['databaseName']]])
  AdminConfig.create('J2EEResourceProperty', propertySet, [['name', 'serverName'], ['type', 'java.lang.String'],
    ['value', param['serverName']]])
  AdminConfig.create('J2EEResourceProperty', propertySet, [['name', 'portNumber'], ['type', 'java.lang.Integer'],
    ['value', param['portNumber']]])


def createJdbcProvider(param):
  printTypeName('JDBC provider', param)
  providerName = param['name']
  provider = AdminConfig.getid("/Node:%s/JDBCProvider/%s" % (nodeName, providerName))
  attrs = [['name', param['name']],
    ['classpath', param['classpath']],
    ['implementationClassName', param['implementationClassName']],
    ['description', param['description']]]

  provider = AdminConfig.create('JDBCProvider', node, attrs)
  createDataSource(param['dataSource'], provider)


def createVariable(param):
  printTypeName('variable', param)
  variables = AdminConfig.list('VariableSubstitutionEntry', node).split(separator)
  for variable in variables:
    if param['name'] == showAttribute(variable, 'symbolicName'):
      AdminConfig.modify(variable, [['value', param['value']]])
      return
  map = AdminConfig.getid("/Node:%s/VariableMap:/" % nodeName)
  AdminConfig.create('VariableSubstitutionEntry', map, [['symbolicName', param['name']], ['value', param['value']]])


def createCredential(param):
  printTypeName('credentials', param)
  security = AdminConfig.getid("/Cell:%sCell/Security:/" % nodeName)
  authAlias = "%s/%s" % (nodeName, param['name'])
  AdminConfig.create('JAASAuthData', security, [['alias', authAlias], ['userId', param['username']], ['password',
    param['password']], ['description', '']])
  print "NOTE: REQUIRES SERVER RESTART"


print dict['node']['name']

# createCredential(dict['node']['j2c'])
# createVariable(dict['node']['variable'])
createJdbcProvider(dict['node']['jdbc'])

AdminConfig.save()