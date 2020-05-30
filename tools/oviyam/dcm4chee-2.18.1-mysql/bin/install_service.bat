@echo off
setlocal
set DIRNAME=%~dp0
set PROGNAME=%~nx0%
pushd %DIRNAME%..
set JBOSS_HOME=%CD%
popd

set RUNJAR=%JBOSS_HOME%\bin\run.jar
if exist "%RUNJAR%" goto found_runjar
echo Could not locate %RUNJAR%. Please check that you are in the
echo bin directory when running this script.
goto eof

:found_runjar
if "%1" == "uninstall" goto uninstall
if "%1" == "server" goto install
if "%1" == "client" goto install
echo "Usage: %0 server|client|uninstall"
echo "Options:"
echo "  client    install DCM4CHEE Image Archive with client hotspot vm"
echo "  server    install DCM4CHEE Image Archive with server hotspot vm"
echo "  uninstall uninstall DCM4CHEE Image Archive service"
goto eof

:install
if not "%JAVA_HOME%" == "" goto found_javahome
echo set JAVA_HOME to your JDK 1.5 installation directory
goto eof

:found_javahome
set VM=%JAVA_HOME%\bin\%1\jvm.dll
if exist "%VM%" goto found_vm
set VM=%JAVA_HOME%\jre\bin\%1\jvm.dll
if exist "%VM%" goto found_vm
echo Could not locate %VM%. Please check that JAVA_HOME is set to your
echo JDK 1.5 installation directory
goto eof

:found_vm
set TOOLS_JAR=%JAVA_HOME%\lib\tools.jar
if exist "%TOOLS_JAR%" goto install
echo Could not locate %TOOLS_JAR%. Unexpected results may occur.
echo Make sure that JAVA_HOME points to a JDK and not a JRE.

:install
rem Setup JBoss specific properties
set JAVA_OPTS=%JAVA_OPTS% -Dprogram.name=%PROGNAME%

rem JVM memory allocation pool parameters. Modify as appropriate.
set JAVA_OPTS=%JAVA_OPTS% -Xms128m -Xmx512m -XX:MaxPermSize=128m

rem With Sun JVMs reduce the RMI GCs to once per hour
set JAVA_OPTS=%JAVA_OPTS% -Dsun.rmi.dgc.client.gcInterval=3600000 -Dsun.rmi.dgc.server.gcInterval=3600000

rem Specify the ID of the ServerPeer used by JBoss Messaging. Must be unique per JBoss instance
set JAVA_OPTS=%JAVA_OPTS% -Djboss.messaging.ServerPeerID=0

rem Use Compiling XSLT Processor (XSLTC)
set JAVA_OPTS=%JAVA_OPTS% -Djavax.xml.transform.TransformerFactory=com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl

rem Set java.library.path to find native jai-imageio components 
set JAVA_OPTS=%JAVA_OPTS% -Djava.library.path=%JBOSS_HOME%\bin\native

rem Set app.name used in emitted audit log messages
set JAVA_OPTS=%JAVA_OPTS% -Dapp.name=dcm4chee

rem Setup the java endorsed dirs
set JAVA_OPTS=%JAVA_OPTS% -Djava.endorsed.dirs=%JBOSS_HOME%\lib\endorsed

rem Enable remote access to jboss services and web interface
set START_PARAMS=-params -b 0.0.0.0

JavaService.exe -install "DCM4CHEE Image Archive" "%VM%"^
  %JAVA_OPTS% "-Djava.class.path=%TOOLS_JAR%;%RUNJAR%"^
  -start org.jboss.Main %START_PARAMS%^
  -stop org.jboss.Main -method systemExit^
  -out "%JBOSS_HOME%\bin\out.txt"^
  -err "%JBOSS_HOME%\bin\err.txt"^
  -current "%JBOSS_HOME%\bin"^
  -path "%JBOSS_HOME%\bin"
goto eof

:uninstall
JavaService.exe -uninstall "DCM4CHEE Image Archive"
goto eof

:eof
endlocal
