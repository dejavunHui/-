#!/bin/sh
DIRNAME=`dirname $0`
SED_OPTS="-i.BAK";

AuditLogger="s/SyslogHost/AuditRepositoryHostname/g"
AuditLogger="$AuditLogger;s/SyslogPort/AuditRepositoryPort/g"
AuditLogger="$AuditLogger;s/Facility/AuditRepositoryFacility/g"
AuditLogger="$AuditLogger;s/SupressLogForAETs/SupressLogForAETitles/g"

sed $SED_OPTS -e "$AuditLogger" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DAuditLogger.xml

CompressionService="s/TempDir/TempDirectory/g"
CompressionService="$CompressionService;s/AutoPurge/AutoDelete/g"

sed $SED_OPTS -e "$CompressionService" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DCompressionService.xml	

ContentEditService="s/CalledAET/CalledAETitle/g"
ContentEditService="$ContentEditService;s/CallingAET/CallingAETitle/g"

sed $SED_OPTS -e "$ContentEditService" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DContentEditService.xml	

DcmServer="s/Port/TCPPort/g"
DcmServer="$DcmServer;s/ProtocolName/SecurityProtocol/g"
DcmServer="$DcmServer;s/DimseTimeout/DIMSETimeout/g"
DcmServer="$DcmServer;s/RqTimeout/RequestTimeout/g"
DcmServer="$DcmServer;s/SoCloseDelay/SocketCloseDelay/g"
DcmServer="$DcmServer;s/MaxPDULength/MaximumPDULength/g"
DcmServer="$DcmServer;s/MaxClients/MaximumDICOMClients/g"
DcmServer="$DcmServer;s/NumClients/CurrentClients/g"
DcmServer="$DcmServer;s/MaxIdleThreads/MaximumIdleThreads/g"
DcmServer="$DcmServer;s/NumIdleThread/CurrentIdleThreads/g"

sed $SED_OPTS -e "$DcmServer" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DDcmServer.xml
	
ECHOService="s/CallingAET/CallingAETitle/g"

sed $SED_OPTS -e "$ECHOService" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DECHOService.xml	

Forward="s/ForwardModifiedToAETs/ForwardModifiedToAETitles/g"
Forward="$Forward;s/MaxSOPInstanceUIDsPerMoveRQ/MaximumSOPInstanceUIDs/g"

sed $SED_OPTS -e "$Forward" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DForward.xml
	
FileSystemMgt="s/DirectoryPathList/DirectoryPaths/g"
FileSystemMgt="$FileSystemMgt;s/ReadOnlyDirectoryPathList/ReadOnlyDirectoryPaths/g"
FileSystemMgt="$FileSystemMgt;s/RetrieveAET/RetrieveAETitle/g"
FileSystemMgt="$FileSystemMgt;s/MinFreeDiskSpace/MinimumFreeDiskSpace/g"
FileSystemMgt="$FileSystemMgt;s/FlushStudiesExternalRetrievable/DeleteStudiesExternallyRetrievable/g"
FileSystemMgt="$FileSystemMgt;s/FlushStudiesOnMedia/DeleteLocalStudiesStoredOnMedia/g"
FileSystemMgt="$FileSystemMgt;s/DeleteStudiesStorageNotCommited/DeleteStudiesFromSystem/g"
FileSystemMgt="$FileSystemMgt;s/StudyCacheTimeout/StudyAgeForDeletion/g"
FileSystemMgt="$FileSystemMgt;s/PurgeFilesInterval/DeleteFilesInterval/g"
FileSystemMgt="$FileSystemMgt;s/PurgeFilesLimit/DeleteFilesLimit/g"
FileSystemMgt="$FileSystemMgt;s/PurgeFilesAfterFreeDiskSpace/DeleteFilesAfterFreeDiskSpace/g"

sed $SED_OPTS -e "$FileSystemMgt" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DFileSystemMgt.xml

GPWLScpService="s/CalledAETs/CalledAETitles/g"
GPWLScpService="$GPWLScpService;s/CallingAETs/CallingAETitles/g"
GPWLScpService="$GPWLScpService;s/MaxPDULength/MaximumPDULength/g"

sed $SED_OPTS -e "$GPWLScpService" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DGPWLScpService.xml
	
IANScu="s/NotifiedAETs/NotifiedAETitles/g"
IANScu="$IANScu;s/CallingAET/CallingAETitle/g"
IANScu="$IANScu;s/RetryIntervalls/RetryIntervals/g"
IANScu="$IANScu;s/ScnPriority/StudyContentNotificationPriority/g"
IANScu="$IANScu;s/AcTimeout/AcceptTimeout/g"
IANScu="$IANScu;s/DimseTimeout/DIMSETimeout/g"
IANScu="$IANScu;s/SoCloseDelay/SocketCloseDelay/g"

sed $SED_OPTS -e "$IANScu" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DIANScu.xml
	
MCMScu="s/CallingAET/CallingAETitle/g"
MCMScu="$MCMScu;s/RetrieveAET/RetrieveAETitle/g"
MCMScu="$MCMScu;s/MoveDestinationAET/MoveDestinationAETitle/g"
MCMScu="$MCMScu;s/McmScpAET/McmScpAETitle/g"
MCMScu="$MCMScu;s/NrOfCopies/NumberOfCopies/g"
MCMScu="$MCMScu;s/AcTimeout/AcceptTimeout/g"
MCMScu="$MCMScu;s/DimseTimeout/DIMSETimeout/g"
MCMScu="$MCMScu;s/SoCloseDelay/SocketCloseDelay/g"
MCMScu="$MCMScu;s/MaxPDUlen/MaximumPDULength/g"

sed $SED_OPTS -e "$MCMScu" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMCMScu.xml
	
MD5CheckService="s/LimitNumberOfFilesPerTask/NumberOfFilesPerCheck/g"

sed $SED_OPTS -e "$MD5CheckService" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMD5CheckService.xml
	
MoveScu="s/CallingAET/CallingAETitle/g"
MoveScu="$MoveScu;s/CalledAET/CalledAETitle/g"
MoveScu="$MoveScu;s/RetryIntervalls/RetryIntervals/g"
MoveScu="$MoveScu;s/AcTimeout/AcceptTimeout/g"
MoveScu="$MoveScu;s/DimseTimeout/DIMSETimeout/g"
MoveScu="$MoveScu;s/SoCloseDelay/SocketCloseDelay/g"

sed $SED_OPTS -e "$MoveScu" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMoveScu.xml
	
MPPSEmulator="s/StationAETsWithDelay/StationAETitlesWithDelay/g"
MPPSEmulator="$MPPSEmulator;s/PollIntervall/PollInterval/g"
MPPSEmulator="$MPPSEmulator;s/CalledAET/CalledAETitle/g"

sed $SED_OPTS -e "$MPPSEmulator" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMPPSEmulator.xml
	
MPPSScp="s/CalledAETs/CalledAETitles/g"
MPPSScp="$MPPSScp;s/CallingAETs/CallingAETitles/g"
MPPSScp="$MPPSScp;s/MaxPDULength/MaximumPDULength/g"

sed $SED_OPTS -e "$MPPSScp" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMPPSScp.xml
	
MPPSScu="s/ForwardAETs/ForwardAETitles/g"
MPPSScu="$MPPSScu;s/CallingAET/CallingAETitle/g"
MPPSScu="$MPPSScu;s/RetryIntervalls/RetryIntervals/g"
MPPSScu="$MPPSScu;s/AcTimeout/AcceptTimeout/g"
MPPSScu="$MPPSScu;s/DimseTimeout/DIMSETimeout/g"
MPPSScu="$MPPSScu;s/SoCloseDelay/SocketCloseDelay/g"

sed $SED_OPTS -e "$MPPSScu" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMPPSScu.xml
	
MWLFindScp="s/MaxPDULength/MaximumPDULength/g"

sed $SED_OPTS -e "$MWLFindScp" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMWLFindScp.xml

MWLScu="s/CalledAET/CalledAETitle/g"
MWLScu="$MWLScu;s/CallingAET/CallingAETitle/g"
MWLScu="$MWLScu;s/AcTimeout/AcceptTimeout/g"
MWLScu="$MWLScu;s/DimseTimeout/DIMSETimeout/g"
MWLScu="$MWLScu;s/SoCloseDelay/SocketCloseDelay/g"
MWLScu="$MWLScu;s/MaxPDULength/MaximumPDULength/g"

sed $SED_OPTS -e "$MWLScu" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DMWLScu.xml
	
PPSScp="s/CalledAETs/CalledAETitles/g"
PPSScp="$PPSScp;s/CallingAETs/CallingAETitles/g"
PPSScp="$PPSScp;s/MaxPDULength/MaximumPDULength/g"

sed $SED_OPTS -e "$PPSScp" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DPPSScp.xml
	
PPSScu="s/ForwardAETs/ForwardAETitles/g"
PPSScu="$PPSScu;s/CallingAET/CallingAETitle/g"
PPSScu="$PPSScu;s/RetryIntervalls/RetryIntervals/g"
PPSScu="$PPSScu;s/AcTimeout/AcceptTimeout/g"
PPSScu="$PPSScu;s/DimseTimeout/DIMSETimeout/g"
PPSScu="$PPSScu;s/SoCloseDelay/SocketCloseDelay/g"

sed $SED_OPTS -e "$PPSScu" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DPPSScu.xml
	
QueryRetrieveScp="s/CalledAETs/CalledAETitles/g"
QueryRetrieveScp="$QueryRetrieveScp;s/CallingAETs/CallingAETitles/g"
QueryRetrieveScp="$QueryRetrieveScp;s/SendNoPixelDataToAETs/SendNoPixelDataToAETitles/g"
QueryRetrieveScp="$QueryRetrieveScp;s/IgnoreUnsupportedSOPClassFailuresByAETs/IgnoreUnsupportedSOPClassFailures/g"
QueryRetrieveScp="$QueryRetrieveScp;s/RequestStgCmtFromAETs/RequestStorageCommitFromAETitles/g"
QueryRetrieveScp="$QueryRetrieveScp;s/MaxBlockedFindRSP/MaximumBlockedFindResponse/g"
QueryRetrieveScp="$QueryRetrieveScp;s/MaxUIDsPerMoveRQ/MaximumUIDsPerMoveRequest/g"
QueryRetrieveScp="$QueryRetrieveScp;s/MaxPDULength/MaximumPDULength/g"
QueryRetrieveScp="$QueryRetrieveScp;s/AcTimeout/AcceptTimeout/g"
QueryRetrieveScp="$QueryRetrieveScp;s/DimseTimeout/DIMSETimeout/g"
QueryRetrieveScp="$QueryRetrieveScp;s/SoCloseDelay/SocketCloseDelay/g"
QueryRetrieveScp="$QueryRetrieveScp;s/EjbProviderURL/EJBProviderURL/g"

sed $SED_OPTS -e "$QueryRetrieveScp" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DQueryRetrieveScp.xml

Sendmail="s/SmtpAuth/SmtpAuthentication/g"
Sendmail="$Sendmail;s/RetryIntervalls/RetryIntervals/g"

sed $SED_OPTS -e "$Sendmail" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DSendmail.xml
	
StgCmtScuScp="s/CalledAETs/CalledAETitles/g"
StgCmtScuScp="$StgCmtScuScp;s/CallingAETs/CallingAETitles/g"
StgCmtScuScp="$StgCmtScuScp;s/ReceiveResultInSameAssocTimeout/ReceiveResultInSameAssociationTimeout/g"
StgCmtScuScp="$StgCmtScuScp;s/ScuRetryIntervalls/SCURetryIntervals/g"
StgCmtScuScp="$StgCmtScuScp;s/ScpRetryIntervalls/SCPRetryIntervals/g"
StgCmtScuScp="$StgCmtScuScp;s/MaxPDULength/MaximumPDULength/g"
StgCmtScuScp="$StgCmtScuScp;s/AcTimeout/AcceptTimeout/g"
StgCmtScuScp="$StgCmtScuScp;s/DimseTimeout/DIMSETimeout/g"
StgCmtScuScp="$StgCmtScuScp;s/SoCloseDelay/SocketCloseDelay/g"
StgCmtScuScp="$StgCmtScuScp;s/EjbProviderURL/EJBProviderURL/g"

sed $SED_OPTS -e "$StgCmtScuScp" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DStgCmtScuScp.xml
	
StoreScp="s/CalledAETs/CalledAETitles/g"
StoreScp="$StoreScp;s/CallingAETs/CallingAETitles/g"
StoreScp="$StoreScp;s/CoerceWarnCallingAETs/WarnForCoercedAETitles/g"
StoreScp="$StoreScp;s/StoreDuplicateIfDiffMD5/StoreDuplicatesIfDifferentMD5/g"
StoreScp="$StoreScp;s/StoreDuplicateIfDiffHost/StoreDuplicatesIfDifferentMD5/g"
StoreScp="$StoreScp;s/UpdateDatabaseMaxRetries/UpdateDatabaseMaximumRetries/g"
StoreScp="$StoreScp;s/MaxCountUpdateDatabaseRetries/UpdateDatabasePerformedRetries/g"
StoreScp="$StoreScp;s/ImageCUIDs/AcceptedImageSOPClasses/g"
StoreScp="$StoreScp;s/OtherCUIDs/AcceptedOtherSOPClasses/g"
StoreScp="$StoreScp;s/MaxPDULength/MaximumPDULength/g"
StoreScp="$StoreScp;s/EjbProviderURL/EJBProviderURL/g"

sed $SED_OPTS -e "$StoreScp" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DStoreScp.xml
	
StudyMgtScp="s/CalledAETs/CalledAETitles/g"
StudyMgtScp="$StudyMgtScp;s/CallingAETs/CallingAETitles/g"
StudyMgtScp="$StudyMgtScp;s/MaxPDULength/MaximumPDULength/g"

sed $SED_OPTS -e "$StudyMgtScp" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DStudyMgtScp.xml
	
StudyMgtScu="s/CallingAET/CalledAETitle/g"
StudyMgtScu="$StudyMgtScu;s/RetryIntervalls/RetryIntervals/g"
StudyMgtScu="$StudyMgtScu;s/AcTimeout/AcceptTimeout/g"
StudyMgtScu="$StudyMgtScu;s/DimseTimeout/DIMSETimeout/g"
StudyMgtScu="$StudyMgtScu;s/SoCloseDelay/SocketCloseDelay/g"

sed $SED_OPTS -e "$StudyMgtScu" \
	$DIRNAME/../server/pacs/data/xmbean-attrs/tiani.archive@3Aservice@3DStudyMgtScu.xml
	
	
