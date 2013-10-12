# wasbear

wsadmin uses Jython 2.1 http://pic.dhe.ibm.com/infocenter/wasinfo/v6r1/index.jsp?topic=%2Fcom.ibm.websphere.express
.doc%2Finfo%2Fexp%2Fae%2Fcxml_jython.html, from 2002.

	wsadmin.sh -user wasadmin -password p@ssw0rd -lang jython -f /wasbear/script.py /wasbear/config.dict

Show required attributes with `print AdminConfig.required('ResourceEnvironmentProvider')`.
