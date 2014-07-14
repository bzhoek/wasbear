# wasbear

wsadmin uses [Jython 2.1](http://pic.dhe.ibm.com/infocenter/wasinfo/v6r1/index.jsp?topic=%2Fcom.ibm.websphere.express
.doc%2Finfo%2Fexp%2Fae%2Fcxml_jython.html), from 2002.

    $ wsadmin.sh -user wasadmin -password p@ssw0rd -lang jython -wsadmin_classpath ./gson-2.2.4.jar -f /wasbear/wasbear.py /wasbear/server.json

Show required attributes with `print AdminConfig.required('ResourceEnvironmentProvider')`.

# wsadmin

    $ rlwrap wsadmin.sh -user wasadmin -password p@ssw0rd -lang jython -wsadmin_classpath ./gson-2.2.4.jar
    > print AdminConfig.help()
    > print AdminConfig.help('remove')
    > print AdminApp.taskInfo('/vagrant/some.ear', 'MapResEnvRefToRes')
    > AdminApp.install('/vagrant/some.ear')

If you have a working manual configuration, you can inspect the configuration objec to ensure you have all the
necessary attributes with

    print AdminConfig.showall(AdminConfig.getid('/DataSource:userDataSource/'))

## wsadmin JSON

Use the -wsadmin_classpath [command-line argument](http://www-01.ibm.com/support/knowledgecenter/?lang=en#!/SSAW57_7.0.0/com.ibm.websphere.nd.multiplatform.doc/info/ae/ae/rxml_commandline.html?cp=SSAW57_7.0.0%2F3-16-1-96)
to include `gson-2.2.4.jar`

# links

http://wdr.github.io/WDR/
http://www.programmingforliving.com/2013/04/was85-application-deployment-using.html
http://mattdowell.blogspot.nl/2008/06/scripting-websphere-61-configurations_23.html

# Jython
http://www.jython.org/archive/21/
http://myarch.com/using-jython-221-with-wsadmin-tool/

# Java
http://www.jython.org/jythonbook/en/1.0/JythonAndJavaIntegration.html

from java.lang import System
System.getProperty("java.version")
