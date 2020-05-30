@echo off
rem -------------------------------------------------------------------------
rem copy needed JBOSS components into DCM4CHEE installation
rem -------------------------------------------------------------------------

if "%OS%" == "Windows_NT"  setlocal
set DIRNAME=.\
if "%OS%" == "Windows_NT" set DIRNAME=%~dp0%

set DCM4CHEE_HOME=%DIRNAME%..
set DCM4CHEE_SERV=%DCM4CHEE_HOME%\server\default

if exist "%DCM4CHEE_SERV%" goto found_dcm4chee
echo Could not locate %DCM4CHEE_SERV%. Please check that you are in the
echo bin directory when running this script.
goto end

:found_dcm4chee
if not [%1] == [] goto found_arg1
echo "Usage: install_jboss <path-to-jboss-4.2.3.GA-installation-directory>"
goto end

:found_arg1
set JBOSS_HOME=%1
set JBOSS_SERV=%JBOSS_HOME%\server\default

if exist "%JBOSS_SERV%" goto found_jboss
echo Could not locate jboss-4.2.3.GA in %JBOSS_HOME%.
goto end

:found_jboss
set JBOSS_BIN=%JBOSS_HOME%\bin
set DCM4CHEE_BIN=%DCM4CHEE_HOME%\bin

copy "%JBOSS_BIN%\run.jar" "%DCM4CHEE_BIN%"
copy "%JBOSS_BIN%\shutdown.bat" "%DCM4CHEE_BIN%"
copy "%JBOSS_BIN%\shutdown.jar" "%DCM4CHEE_BIN%"
copy "%JBOSS_BIN%\shutdown.sh" "%DCM4CHEE_BIN%"
copy "%JBOSS_BIN%\twiddle.bat" "%DCM4CHEE_BIN%"
copy "%JBOSS_BIN%\twiddle.jar" "%DCM4CHEE_BIN%"
copy "%JBOSS_BIN%\twiddle.sh" "%DCM4CHEE_BIN%"

md "%DCM4CHEE_HOME%\client"
copy "%JBOSS_HOME%\client\jbossall-client.jar" "%DCM4CHEE_HOME%\client"
copy "%JBOSS_HOME%\client\getopt.jar" "%DCM4CHEE_HOME%\client"

xcopy /S "%JBOSS_HOME%\lib" "%DCM4CHEE_HOME%\lib\"

set JBOSS_CONF=%JBOSS_SERV%\conf
set DCM4CHEE_CONF=%DCM4CHEE_SERV%\conf
copy "%JBOSS_CONF%\jbossjta-properties.xml" "%DCM4CHEE_CONF%"
copy "%JBOSS_CONF%\jndi.properties" "%DCM4CHEE_CONF%"
xcopy /S "%JBOSS_CONF%\props" "%DCM4CHEE_CONF%\props\"
xcopy /S "%JBOSS_CONF%\xmdesc" "%DCM4CHEE_CONF%\xmdesc\"

xcopy /S "%JBOSS_SERV%\lib" "%DCM4CHEE_SERV%\lib\"
del "%DCM4CHEE_SERV%\lib\jbossmq.jar"

set JBOSS_DEPLOY=%JBOSS_SERV%\deploy
set DCM4CHEE_DEPLOY=%DCM4CHEE_SERV%\deploy

copy "%JBOSS_DEPLOY%\bsh-deployer.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\cache-invalidation-service.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\client-deployer-service.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\ear-deployer.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\ejb3-interceptors-aop.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\jboss-ha-local-jdbc.rar" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\jboss-ha-xa-jdbc.rar" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\jbossjca-service.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\jboss-local-jdbc.rar" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\jboss-xa-jdbc.rar" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\jsr88-service.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\mail-service.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\properties-service.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\quartz-ra.rar" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\sqlexception-service.xml" "%DCM4CHEE_DEPLOY%"
copy "%JBOSS_DEPLOY%\jms\jms-ra.rar" "%DCM4CHEE_DEPLOY%"

xcopy /S "%JBOSS_DEPLOY%\ejb3.deployer" "%DCM4CHEE_DEPLOY%\ejb3.deployer\"
xcopy /S "%JBOSS_DEPLOY%\http-invoker.sar" "%DCM4CHEE_DEPLOY%\http-invoker.sar\"
xcopy /S "%JBOSS_DEPLOY%\jboss-aop-jdk50.deployer" "%DCM4CHEE_DEPLOY%\jboss-aop-jdk50.deployer\"
xcopy /S "%JBOSS_DEPLOY%\jboss-bean.deployer" "%DCM4CHEE_DEPLOY%\jboss-bean.deployer\"
xcopy /S "%JBOSS_DEPLOY%\jbossws.sar" "%DCM4CHEE_DEPLOY%\jbossws.sar\"
move "%DCM4CHEE_DEPLOY%"\jbossws.sar\jaxb-api.jar "%DCM4CHEE_SERV%"\lib\"
move "%DCM4CHEE_DEPLOY%"\jbossws.sar\jaxb-impl.jar "%DCM4CHEE_SERV%"\lib\"

set JBOSS_WEB=%JBOSS_DEPLOY%\jboss-web.deployer
set DCM4CHEE_WEB=%DCM4CHEE_DEPLOY%\jboss-web.deployer

copy "%JBOSS_WEB%\context.xml" "%DCM4CHEE_WEB%"
copy "%JBOSS_WEB%\jasper-jdt.jar" "%DCM4CHEE_WEB%"
copy "%JBOSS_WEB%\jbossweb-extras.jar" "%DCM4CHEE_WEB%"
copy "%JBOSS_WEB%\jbossweb.jar" "%DCM4CHEE_WEB%"
copy "%JBOSS_WEB%\jbossweb-service.jar" "%DCM4CHEE_WEB%"
copy "%JBOSS_WEB%\jstl.jar" "%DCM4CHEE_WEB%"

xcopy /S "%JBOSS_WEB%\conf" "%DCM4CHEE_WEB%\conf\"
xcopy /S "%JBOSS_WEB%\jsf-libs" "%DCM4CHEE_WEB%\jsf-libs\"
xcopy /S "%JBOSS_WEB%\META-INF" "%DCM4CHEE_WEB%\META-INF\"
xcopy /S "%JBOSS_WEB%\ROOT.war" "%DCM4CHEE_WEB%\ROOT.war\"

set JBOSS_JMX_CONSOLE=%JBOSS_DEPLOY%\jmx-console.war
set DCM4CHEE_JMX_CONSOLE=%DCM4CHEE_DEPLOY%\jmx-console.war

copy "%JBOSS_JMX_CONSOLE%\checkJNDI.jsp" "%DCM4CHEE_JMX_CONSOLE%"
copy "%JBOSS_JMX_CONSOLE%\displayMBeans.jsp" "%DCM4CHEE_JMX_CONSOLE%"
copy "%JBOSS_JMX_CONSOLE%\displayOpResult.jsp" "%DCM4CHEE_JMX_CONSOLE%"
copy "%JBOSS_JMX_CONSOLE%\index.jsp" "%DCM4CHEE_JMX_CONSOLE%"
copy "%JBOSS_JMX_CONSOLE%\jboss.css" "%DCM4CHEE_JMX_CONSOLE%"
copy "%JBOSS_JMX_CONSOLE%\style_master.css" "%DCM4CHEE_JMX_CONSOLE%"

xcopy /S "%JBOSS_JMX_CONSOLE%\cluster" "%DCM4CHEE_JMX_CONSOLE%\cluster\"
xcopy /S "%JBOSS_JMX_CONSOLE%\images" "%DCM4CHEE_JMX_CONSOLE%\images\"
xcopy /S "%JBOSS_JMX_CONSOLE%\META-INF" "%DCM4CHEE_JMX_CONSOLE%\META-INF\"

xcopy /S "%JBOSS_JMX_CONSOLE%\WEB-INF\classes" "%DCM4CHEE_JMX_CONSOLE%\WEB-INF\classes\"

set JBOSS_CONSOLE_MGR=%JBOSS_DEPLOY%\management\console-mgr.sar
set DCM4CHEE_CONSOLE_MGR=%DCM4CHEE_DEPLOY%\management\console-mgr.sar

copy "%JBOSS_CONSOLE_MGR%\*.jar" "%DCM4CHEE_CONSOLE_MGR%"

xcopy /S "%JBOSS_CONSOLE_MGR%\META-INF" "%DCM4CHEE_CONSOLE_MGR%\META-INF\"

set JBOSS_WEB_CONSOLE=%JBOSS_CONSOLE_MGR%\web-console.war
set DCM4CHEE_WEB_CONSOLE=%DCM4CHEE_CONSOLE_MGR%\web-console.war

copy "%JBOSS_WEB_CONSOLE%\*.html" "%DCM4CHEE_WEB_CONSOLE%"
copy "%JBOSS_WEB_CONSOLE%\*.jar" "%DCM4CHEE_WEB_CONSOLE%"
copy "%JBOSS_WEB_CONSOLE%\*.js" "%DCM4CHEE_WEB_CONSOLE%"
copy "%JBOSS_WEB_CONSOLE%\*.jsp" "%DCM4CHEE_WEB_CONSOLE%"

xcopy /S "%JBOSS_WEB_CONSOLE%\css" "%DCM4CHEE_WEB_CONSOLE%\css\"
xcopy /S "%JBOSS_WEB_CONSOLE%\images" "%DCM4CHEE_WEB_CONSOLE%\images\"
xcopy /S "%JBOSS_WEB_CONSOLE%\img" "%DCM4CHEE_WEB_CONSOLE%\img\"
xcopy /S "%JBOSS_WEB_CONSOLE%\META-INF" "%DCM4CHEE_WEB_CONSOLE%\META-INF\"

xcopy /S "%JBOSS_WEB_CONSOLE%\WEB-INF\classes" "%DCM4CHEE_WEB_CONSOLE%\WEB-INF\classes\"
xcopy /S "%JBOSS_WEB_CONSOLE%\WEB-INF\tlds" "%DCM4CHEE_WEB_CONSOLE%\WEB-INF\tlds\"

:end
if "%OS%" == "Windows_NT" endlocal
