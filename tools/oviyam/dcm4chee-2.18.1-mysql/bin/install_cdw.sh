#!/bin/sh
# -------------------------------------------------------------------------
# copy DCM4CHEE Media Creator components into DCM4CHEE Archive installation
# -------------------------------------------------------------------------

DIRNAME=`dirname $0`
DCM4CHEE_HOME="$DIRNAME"/..
DCM4CHEE_SERV="$DCM4CHEE_HOME"/server/default

if [ x$1 = x ]; then
  echo "Usage: $0 <path-to-dcm4chee-cdw-installation-directory>"
  exit 1
fi

CDW_HOME="$1"
CDW_SERV="$CDW_HOME"/server/default

if [ ! -d "$CDW_SERV"/conf/dcm4chee-cdw ]; then
  echo Could not locate dcm4chee-cdw in "$CDW_HOME"
  exit 1
fi

cp -v "$CDW_HOME"/bin/acroread.bat \
  "$CDW_HOME"/bin/fop.bat \
  "$CDW_HOME"/bin/fop.sh \
  "$CDW_HOME"/bin/fop.xconf \
  "$CDW_HOME"/bin/xalan.bat \
  "$CDW_HOME"/bin/xalan.sh \
  "$DCM4CHEE_HOME"/bin

cp -v -R "$CDW_SERV"/conf/dcm4chee-auditlog \
  "$CDW_SERV"/conf/dcm4chee-cdw \
  "$CDW_SERV"/conf/xmdesc \
  "$DCM4CHEE_SERV"/conf

if [ ! -d "$DCM4CHEE_SERV"/data ]; then
  mkdir "$DCM4CHEE_SERV"/data
fi

cp -v -R "$CDW_SERV"/data/mergedir \
  "$CDW_SERV"/data/mergedir-viewer \
  "$CDW_SERV"/data/mergedir-web \
  "$DCM4CHEE_SERV"/data
  
cp -v "$CDW_SERV"/deploy/dcm4chee-cdrecord.sar \
  "$CDW_SERV"/deploy/dcm4chee-cdw.sar \
  "$CDW_SERV"/deploy/dcm4chee-nerocmd.sar \
  "$DCM4CHEE_SERV"/deploy
  
cp -v "$CDW_SERV"/lib/dcm4chee-cdw.jar "$DCM4CHEE_SERV"/lib
