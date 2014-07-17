# wasbear

Apply JSON based configuration in an idempotent manner.

## wsadmin

wsadmin uses [Jython 2.1](http://pic.dhe.ibm.com/infocenter/wasinfo/v6r1/index.jsp?topic=%2Fcom.ibm.websphere.express
.doc%2Finfo%2Fexp%2Fae%2Fcxml_jython.html), from 2002.

    $ wsadmin.sh -user wasadmin -password p@ssw0rd -lang jython -wsadmin_classpath /wasbear/gson-2.2.4.jar -f /wasbear/wasbear.py /wasbear/server.json

    $ rlwrap wsadmin.sh -user wasadmin -password p@ssw0rd -lang jython -wsadmin_classpath ./gson-2.2.4.jar
    > print AdminConfig.help()
    > print AdminConfig.help('remove')
    > print AdminApp.taskInfo('/vagrant/some.ear', 'MapResEnvRefToRes')
    > AdminApp.install('/vagrant/some.ear')

If you have a working manual configuration, you can inspect the configuration object to ensure you have all the
necessary attributes with

    print AdminConfig.showall(AdminConfig.getid('/DataSource:userDataSource/'))

Show required attributes with `print AdminConfig.required('ResourceEnvironmentProvider')`.

    print AdminConfig.showall(AdminConfig.list("JavaVirtualMachine", server))

    | process | JavaProcessDef     |
    | java    | JavaVirtualMachine |


### wsadmin JSON

Use the -wsadmin_classpath [command-line argument](http://www-01.ibm.com/support/knowledgecenter/?lang=en#!/SSAW57_7.0.0/com.ibm.websphere.nd.multiplatform.doc/info/ae/ae/rxml_commandline.html?cp=SSAW57_7.0.0%2F3-16-1-96)
to include `gson-2.2.4.jar`

### wsadmin Install WAR

http://www-01.ibm.com/support/docview.wss?uid=swg21199311
http://www.programmingforliving.com/2013/04/was85-application-deployment-using.html

    > AdminApp.install('/wasbear/ecommerce-ahws.war', ['-MapWebModToVH', [['.*', '.*', 'default_host']]])

Genereert zelf een naam, beter is de `-appname` parameter mee te geven.

    > AdminApp.install('/wasbear/ecommerce-ahws.war', ['-reloadInterval ', '11', '-reloadEnabled', 'true', '-appname', 'ecommerce-ahws', '-MapWebModToVH', [['.*', '.*', 'default_host']]])
    > AdminConfig.save()

### wsadmin Documentation
http://www-01.ibm.com/support/knowledgecenter/?lang=en#!/SSEQTP_7.0.0/com.ibm.websphere.base.doc/info/aes/ae/rxml_adminapp.html

## Links

http://wdr.github.io/WDR/
http://www.programmingforliving.com/2013/04/was85-application-deployment-using.html
http://mattdowell.blogspot.nl/2008/06/scripting-websphere-61-configurations_23.html

## Jython
http://www.jython.org/archive/21/
http://myarch.com/using-jython-221-with-wsadmin-tool/

### Java
http://www.jython.org/jythonbook/en/1.0/JythonAndJavaIntegration.html

from java.lang import System
System.getProperty("java.version")

## WebSphere

    ps axuww
    /opt/ibm/websphere/appserver/java/bin/java ... com.ibm.ws.runtime.WsServer /opt/ibm/websphere/appserver/profiles/AppSrv01/config server2Node01Cell server2Node01 server1

### Heap

Default heap is 50M initial, 256M maximum http://www.ibm.com/developerworks/websphere/techjournal/0909_blythe/0909_blythe.html