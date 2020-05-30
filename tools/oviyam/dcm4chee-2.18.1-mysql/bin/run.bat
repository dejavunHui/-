@echo off
rem -------------------------------------------------------------------------
rem JBoss Bootstrap Script for Win32
rem -------------------------------------------------------------------------

rem $Id: run.bat 17856 2013-06-04 10:10:22Z javawilli $

@if not "%ECHO%" == ""  echo %ECHO%
@if "%OS%" == "Windows_NT"  setlocal

set DIRNAME=.\
if "%OS%" == "Windows_NT" set DIRNAME=%~dp0%
set PROGNAME=run.bat
if "%OS%" == "Windows_NT" set PROGNAME=%~nx0%

pushd %DIRNAME%..
set JBOSS_HOME=%CD%
popd

REM Add JBOSS_HOME/bin to the PATH
set PATH=%JBOSS_HOME%\bin;%PATH%

REM Add bin/native to the PATH if present
if exist "%JBOSS_HOME%\bin\native" set PATH=%JBOSS_HOME%\bin\native;%PATH%
if exist "%JBOSS_HOME%\bin\native" set JAVA_OPTS=%JAVA_OPTS% -Djava.library.path="%JBOSS_HOME%\bin\native"

rem Read all command line arguments

REM
REM The %ARGS% env variable commented out in favor of using %* to include
REM all args in java command line. See bug #840239. [jpl]
REM
REM set ARGS=
REM :loop
REM if [%1] == [] goto endloop
REM         set ARGS=%ARGS% %1
REM         shift
REM         goto loop
REM :endloop

rem Find run.jar, or we can't continue

set RUNJAR=%JBOSS_HOME%\bin\run.jar
if exist "%RUNJAR%" goto FOUND_RUN_JAR
echo Could not locate %RUNJAR%. Please check that you are in the
echo bin directory when running this script.
goto END

:FOUND_RUN_JAR

if not "%JAVA_HOME%" == "" goto ADD_TOOLS

set JAVA=java

echo JAVA_HOME is not set.  Unexpected results may occur.
echo Set JAVA_HOME to the directory of your local JDK to avoid this message.
goto SKIP_TOOLS

:ADD_TOOLS

set JAVA=%JAVA_HOME%\bin\java

rem A full JDK with toos.jar is not required anymore since jboss web packages
rem the eclipse jdt compiler and javassist has its own internal compiler.
if not exist "%JAVA_HOME%\lib\tools.jar" goto SKIP_TOOLS

rem If exists, point to the JDK javac compiler in case the user wants to
rem later override the eclipse jdt compiler for compiling JSP pages.
set JAVAC_JAR=%JAVA_HOME%\lib\tools.jar

:SKIP_TOOLS

rem If JBOSS_CLASSPATH or JAVAC_JAR is empty, don't include it, as this will 
rem result in including the local directory in the classpath, which makes
rem error tracking harder.
if not "%JAVAC_JAR%" == "" set RUNJAR=%JAVAC_JAR%;%RUNJAR%
if "%JBOSS_CLASSPATH%" == "" set RUN_CLASSPATH=%RUNJAR%
if "%RUN_CLASSPATH%" == "" set RUN_CLASSPATH=%JBOSS_CLASSPATH%;%RUNJAR%

set JBOSS_CLASSPATH=%RUN_CLASSPATH%

rem Setup JBoss specific properties
set JAVA_OPTS=%JAVA_OPTS% -Dprogram.name=%PROGNAME%

rem Add -server to the JVM options, if supported
"%JAVA%" -version 2>&1 | findstr /I hotspot > nul
if not errorlevel == 1 (set JAVA_OPTS=%JAVA_OPTS% -server)

rem JVM memory allocation pool parameters. Modify as appropriate.
set JAVA_OPTS=%JAVA_OPTS% -Xms128m -Xmx512m -XX:MaxPermSize=128m

rem Specify the ID of the ServerPeer used by JBoss Messaging. Must be unique per JBoss instance
set JAVA_OPTS=%JAVA_OPTS% -Djboss.messaging.ServerPeerID=0

rem Use Compiling XSLT Processor (XSLTC)
set JAVA_OPTS=%JAVA_OPTS% -Djavax.xml.transform.TransformerFactory=com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl

rem Uncomment to enable the jconsole agent locally
rem JAVA_OPTS=%JAVA_OPTS% -Dcom.sun.management.jmxremote
rem Tell JBossAS to use the platform MBean server
rem set JAVA_OPTS=%JAVA_OPTS% -Djboss.platform.mbeanserver
rem Make the platform MBean server able to work with JBossAS MBeans
rem set JAVA_OPTS=%JAVA_OPTS% -Djavax.management.builder.initial=org.jboss.system.server.jmx.MBeanServerBuilderImpl

rem Uncomment to enable the jconsole agent remotely on port 12345 with disabled security and ssl transport
rem set JAVA_OPTS=%JAVA_OPTS% -Dcom.sun.management.jmxremote.port=12345
rem set JAVA_OPTS=%JAVA_OPTS% -Dcom.sun.management.jmxremote.authenticate=false
rem set JAVA_OPTS=%JAVA_OPTS% -Dcom.sun.management.jmxremote.ssl=false

rem With Sun JVMs reduce the RMI GCs to once per hour
set JAVA_OPTS=%JAVA_OPTS% -Dsun.rmi.dgc.client.gcInterval=3600000 -Dsun.rmi.dgc.server.gcInterval=3600000

rem Set app.name used in emitted audit log messages
set JAVA_OPTS=%JAVA_OPTS% -Dapp.name=dcm4chee

rem Set Node Name displayed in web login page
rem (display hostname if dcm4che.archive.nodename isn't set)
rem set JAVA_OPTS=%JAVA_OPTS% -Ddcm4che.archive.nodename=DCM4CHEE

rem JPDA options. Uncomment and modify as appropriate to enable remote debugging.
rem set JAVA_OPTS=-Xdebug -Xrunjdwp:transport=dt_socket,address=8787,server=y,suspend=y %JAVA_OPTS%

rem Setup the java endorsed dirs
set JBOSS_ENDORSED_DIRS=%JBOSS_HOME%\lib\endorsed

rem Enable remote access to jboss services and web interface
if "%JBOSS_BIND_ADDR%" == "" set JBOSS_BIND_ADDR=0.0.0.0

rem Sample SSL debugging option:
rem set JAVA_OPTS=%JAVA_OPTS% -Djavax.net.debug=ssl,handshake,data,trustmanager,help
rem set JAVA_OPTS=%JAVA_OPTS% -Djavax.net.debug=ssl,handshake

echo ===============================================================================
echo.
echo   JBoss Bootstrap Environment
echo.
echo   JBOSS_HOME: %JBOSS_HOME%
echo.
echo   JAVA: %JAVA%
echo.
echo   JAVA_OPTS: %JAVA_OPTS%
echo.
echo   CLASSPATH: %JBOSS_CLASSPATH%
echo.
echo ===============================================================================
echo.

:RESTART
"%JAVA%" %JAVA_OPTS% "-Djava.endorsed.dirs=%JBOSS_ENDORSED_DIRS%" -classpath "%JBOSS_CLASSPATH%" org.jboss.Main -b %JBOSS_BIND_ADDR% %*
if ERRORLEVEL 10 goto RESTART

:END
if "%NOPAUSE%" == "" pause

:END_NO_PAUSE
