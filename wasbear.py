from com.google.gson import JsonObject
from com.google.gson import JsonParser
from com.google.gson import JsonPrimitive
from java.io import FileReader

separator = java.lang.System.getProperty("line.separator")

parser = JsonParser()
infile = (len(sys.argv) == 1) and sys.argv[0] or "config.json"
print "Processing ** '%s' **" % infile

reader = FileReader(infile)
json = parser.parse(reader)
nodeName = json.get('node').get('name')
node = AdminConfig.getid('/Node:%s/' % nodeName)
if not node:
  raise Exception("WebSphere node '%s' not found" % nodeName)


def hasAppName(appName):
  return len(AdminConfig.getid("/Deployment:" + appName + "/")) > 0


def printDeleteName(type, param):
  print "Deleting %s: %s" % (type, param.get('name'))


def printCreateName(type, param):
  print "Creating %s: %s" % (type, param.get('name'))


def showAttribute(object, name):
  return AdminConfig.showAttribute(object, name)


def listify(value):
  if value.class == JsonObject:
    list = []
    [list.append([pair.getKey(), pair.getValue()]) for pair in value.entrySet().toArray()]
    return list
  else:
    return value


def createServer(param):
  def createJavaProcessDefinition(server, param):
    config = AdminConfig.list('JavaProcessDef', server)
    for pair in param.entrySet().toArray():
      AdminConfig.modify(config, [[pair.getKey(), listify(pair.getValue())]])


  def createJavaVirtualMachine(server, param):
    config = AdminConfig.list('JavaVirtualMachine', server)
    for pair in param.entrySet().toArray():
      AdminConfig.modify(config, [[pair.getKey(), pair.getValue()]])

  def createJavaVirtualMachineArguments(server, param):
    config = AdminConfig.list('JavaVirtualMachine', server)
    arguments = []
    for pair in param.entrySet().toArray():
      arguments.append("-D%s=%s" % (pair.getKey(), pair.getValue()))
    AdminConfig.modify(config, [["genericJvmArguments", " ".join(arguments)]])

  def installWebArchive(serverName, param):
    appname = param.get('name').getAsString()
    if hasAppName(appname):
      print "Uninstalling %s" % appname
      AdminApp.uninstall(appname)

    file = param.get('file').getAsString()
    print "Installing file %s as %s" % (file, serverName)
    AdminApp.install(file,
      ['-reloadInterval ', '11', '-reloadEnabled', 'true', '-appname', appname, '-MapWebModToVH',
        [['.*', '.*', 'default_host']]])


  servername = param.get('name')
  serverid = AdminConfig.getid("/Server:%s" % servername)
  if serverid:
    printDeleteName('server', param)
    AdminConfig.remove(serverid)

  if param.get('ensure') and param.get('ensure').getAsString() == "absent":
    return

  printCreateName('server', param)
  server = AdminConfig.create('Server', node, [['name', servername]])

  if param.get('process'):
    createJavaProcessDefinition(server, param.get('process'))

  if param.get('java'):
    createJavaVirtualMachine(server, param.get('java'))

  if param.get('arguments'):
    createJavaVirtualMachineArguments(server, param.get('arguments'))

  if param.get('war'):
    installWebArchive(servername, param.get('war'))


def createDataSource(param, provider):
  printCreateName('data source', param)
  providerName = showAttribute(provider, 'name')
  dataSourceName = param['name']
  dataSource = AdminConfig.getid("/Node:%s/JDBCProvider:%s/DataSource:%s" % (nodeName, providerName, dataSourceName ))
  mapping = ['mapping', [['authDataAlias', param['j2c']], ['mappingConfigAlias', param['mapping']]]]
  attrs = [['name', dataSourceName], ['jndiName', param['jndiName']], ['relationalResourceAdapter',
    findResourceAdapter()], ['datasourceHelperClassname', 'com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper'],
    ['authDataAlias', param['j2c']], mapping]
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
  printCreateName('JDBC provider', param)
  providerName = param['name']
  provider = AdminConfig.getid("/Node:%s/JDBCProvider/%s" % (nodeName, providerName))
  attrs = [['name', param['name']],
    ['classpath', param['classpath']],
    ['implementationClassName', param['implementationClassName']],
    ['description', param['description']],
    ['providerType', 'DB2 Universal JDBC Driver Provider']]

  provider = AdminConfig.create('JDBCProvider', node, attrs)
  createDataSource(param['dataSource'], provider)


def createVariable(param):
  printCreateName('variable', param)
  variables = AdminConfig.list('VariableSubstitutionEntry', node).split(separator)
  for variable in variables:
    if param['name'] == showAttribute(variable, 'symbolicName'):
      AdminConfig.modify(variable, [['value', param['value']]])
      return
  map = AdminConfig.getid("/Node:%s/VariableMap:/" % nodeName)
  AdminConfig.create('VariableSubstitutionEntry', map, [['symbolicName', param['name']], ['value', param['value']]])


def createCredential(param):
  printCreateName('credentials', param)
  security = AdminConfig.getid("/Cell:%sCell/Security:/" % nodeName)
  authAlias = "%s/%s" % (nodeName, param['name'])
  AdminConfig.create('JAASAuthData', security, [['alias', authAlias], ['userId', param['username']], ['password',
    param['password']], ['description', '']])
  print "NOTE: REQUIRES SERVER RESTART"


def installApplication(param):
  virtualHost = [['.*', '.*', param['host']]]
  resource = param['resource']
  dataSource = [['.*', '', '.*', resource['reference'], resource['type'], resource['jndiName'], resource['j2c'], '']]
  AdminApp.install(param['ear'], ['-MapResRefToEJB', dataSource, '-MapWebModToVH', virtualHost])


def findResourceAdapter():
  for adapter in AdminConfig.list('J2CResourceAdapter', node).split(separator):
    if "WebSphere Relational Resource Adapter" == showAttribute(adapter, 'name'):
      return adapter


def asList(node):
  if node.isJsonArray():
    return [node.get(i) for i in range(0, node.size())]
  else:
    return [node]


[createServer(server) for server in asList(json.get('node').get('server'))]

AdminConfig.save()

# installApplication(dict['node']['server']['application'])
# createCredential(dict['node']['j2c'])
# createVariable(dict['node']['variable'])
# createJdbcProvider(dict['node']['jdbc'])


