# Python 2.4

Centos 5.5 has a version of Python that doesn't come with JSON support.

    $ yum install python-pip
    $ easy_install https://pypi.python.org/packages/2.4/s/simplejson/simplejson-1.7-py2.4.egg
  
# wasbear

wsadmin uses [Jython 2.1](http://pic.dhe.ibm.com/infocenter/wasinfo/v6r1/index.jsp?topic=%2Fcom.ibm.websphere.express
.doc%2Finfo%2Fexp%2Fae%2Fcxml_jython.html), from 2002.

    $ python config.py server.json server.dict; wsadmin.sh -user wasadmin -password p@ssw0rd -lang jython -f /wasbear/wasbear.py /wasbear/server.dict

Show required attributes with `print AdminConfig.required('ResourceEnvironmentProvider')`.

# wsadmin

    $ rlwrap wsadmin.sh -user wasadmin -password p@ssw0rd -lang jython
    > print AdminConfig.help()
    > print AdminConfig.help('remove')

`print AdminApp.taskInfo('/vagrant/ics-ear-13.4.0-SNAPSHOT-nl.ear', 'MapResEnvRefToRes')`

AdminApp.install('/vagrant/iwa-usermanagement-server-ear-13.4.0.1-SNAPSHOT.ear')

If you have a working manual configuration, you can inspect the configuration objec to ensure you have all the
necessary attributes with

    print AdminConfig.showall(AdminConfig.getid('/DataSource:userDataSource/'))

# links

http://wdr.github.io/WDR/
http://www.programmingforliving.com/2013/04/was85-application-deployment-using.html
http://mattdowell.blogspot.nl/2008/06/scripting-websphere-61-configurations_23.html