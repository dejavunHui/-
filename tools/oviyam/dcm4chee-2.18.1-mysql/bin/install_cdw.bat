@echo off
rem -------------------------------------------------------------------------
rem copy DCM4CHEE Media Creator components into DCM4CHEE Archive installation
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
echo "Usage: install_cdw <path-to-dcm4chee-cdw-installation-directory>"
goto end

:found_arg1
set CDW_HOME=%1
set CDW_SERV=%CDW_HOME%\server\default

if exist "%CDW_SERV%\conf\dcm4chee-cdw" goto found_cdw
echo Could not locate dcm4chee-cdw in %CDW_HOME%.
goto end

:found_cdw
set CDW_BIN=%CDW_HOME%\bin
set DCM4CHEE_BIN=%DCM4CHEE_HOME%\bin

copy "%CDW_BIN%\acroread.bat" "%DCM4CHEE_BIN%"
copy "%CDW_BIN%\fop.bat" "%DCM4CHEE_BIN%"
copy "%CDW_BIN%\fop.sh" "%DCM4CHEE_BIN%"
copy "%CDW_BIN%\fop.xconf" "%DCM4CHEE_BIN%"
copy "%CDW_BIN%\xalan.bat" "%DCM4CHEE_BIN%"
copy "%CDW_BIN%\xalan.sh" "%DCM4CHEE_BIN%"

set CDW_CONF=%CDW_SERV%\conf
set DCM4CHEE_CONF=%DCM4CHEE_SERV%\conf

xcopy /S "%CDW_CONF%\dcm4chee-audit" "%DCM4CHEE_CONF%\dcm4chee-audit\"
xcopy /S "%CDW_CONF%\dcm4chee-cdw" "%DCM4CHEE_CONF%\dcm4chee-cdw\"
xcopy /S "%CDW_CONF%\xmdesc" "%DCM4CHEE_CONF%\xmdesc\"

set CDW_DATA=%CDW_SERV%\data
set DCM4CHEE_DATA=%DCM4CHEE_SERV%\data

if exist "%DCM4CHEE_DATA%" goto found_dcm4chee_data
md "%DCM4CHEE_DATA%"

:found_dcm4chee_data
xcopy /S "%CDW_DATA%\mergedir" "%DCM4CHEE_DATA%\mergedir\"
xcopy /S "%CDW_DATA%\mergedir-viewer" "%DCM4CHEE_DATA%\mergedir-viewer\"
xcopy /S "%CDW_DATA%\mergedir-web" "%DCM4CHEE_DATA%\mergedir-web\"

set CDW_DEPLOY=%CDW_SERV%\deploy
set DCM4CHEE_DEPLOY=%DCM4CHEE_SERV%\deploy

copy "%CDW_DEPLOY%\dcm4chee-cdrecord.sar" "%DCM4CHEE_DEPLOY%"
copy "%CDW_DEPLOY%\dcm4chee-cdw.sar" "%DCM4CHEE_DEPLOY%"
copy "%CDW_DEPLOY%\dcm4chee-nerocmd.sar" "%DCM4CHEE_DEPLOY%"

copy "%CDW_SERV%\lib\dcm4chee-cdw.jar" "%DCM4CHEE_SERV%\lib"

:end
if "%OS%" == "Windows_NT" endlocal
