#!/bin/sh
# -------------------------------------------------------------------------
# copy XDS components into DCM4CHEE archive installation
# -------------------------------------------------------------------------

DIRNAME=`dirname $0`
DCM4CHEE_HOME="$DIRNAME"/..
DCM4CHEE_SERV="$DCM4CHEE_HOME"/server/default

if [ x$1 = x ]; then
  echo "Usage: $0 <path-to-dcm4chee-xds-installation-directory>"
  exit 1
fi

XDS_HOME="$1"
XDS_SERV="$XDS_HOME"/server/default

if [ ! -f "$XDS_HOME"/bin/upgrade_jbossws.sh ]; then
  echo Could not locate dcm4chee-xds in "$XDS_HOME"
  exit 1
fi

cp -v -R "$XDS_SERV"/deploy/dcm4che* "$DCM4CHEE_SERV"/deploy
cp -v "$XDS_SERV"/conf/xmdesc/dcm4chee-xds-xmbean.xml "$DCM4CHEE_SERV"/conf/xmdesc
cp -v "$XDS_SERV"/lib/* "$DCM4CHEE_SERV"/lib
cp -v "$XDS_HOME"/bin/* "$DCM4CHEE_HOME"/bin

echo XDS components installed!
