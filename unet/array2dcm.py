import pydicom
import numpy

def createDcm(data, date, row, column,pid, innumber, outputfile):
    # File meta info data elements
    file_meta = Dataset()
    file_meta.FileMetaInformationGroupLength = 230
    file_meta.FileMetaInformationVersion = b'\x00\x01'
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    file_meta.MediaStorageSOPInstanceUID = '1.2.826.0.1.3680043.8.1055.1.{}.03296050.69180943'.format(date)
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.4.91'
    file_meta.ImplementationClassUID = '1.2.826.0.1.3680043.8.1055.1'
    file_meta.ImplementationVersionName = 'dicomlibrary-100'
    file_meta.SourceApplicationEntityTitle = 'DICOMLIBRARY'

    # Main data elements
    ds = Dataset()
    ds.SpecificCharacterSet = 'ISO_IR 100'
    ds.ImageType = ['ORIGINAL', 'PRIMARY', 'AXIAL', 'HELIX']
    ds.InstanceCreationDate = '20061012'
    ds.InstanceCreationTime = '091605.000000'
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    ds.SOPInstanceUID = '1.2.826.0.1.3680043.8.1055.1.{}.03296050.69180943'.format(date)
    ds.StudyDate = '20061012'
    ds.AcquisitionDate = date
    ds.ContentDate = date
    ds.StudyTime = '090258.000000'
    ds.AcquisitionTime = '085229.000000'
    ds.ContentTime = '085229.719000'
    ds.Modality = 'CT'
    ds.StudyDescription = 'CT1 abdomen'

    # Procedure Code Sequence
    procedure_code_sequence = Sequence()
    ds.ProcedureCodeSequence = procedure_code_sequence

    # Procedure Code Sequence: Procedure Code 1
    procedure_code1 = Dataset()
    procedure_code1.CodeValue = 'CTABDOM'
    procedure_code1.CodingSchemeDesignator = 'XPLORE'
    procedure_code1.CodeMeaning = 'CT1 abdomen'
    procedure_code_sequence.append(procedure_code1)

    ds.SeriesDescription = 'ARTERIELLE'

    # Referenced Performed Procedure Step Sequence
    refd_performed_procedure_step_sequence = Sequence()
    ds.ReferencedPerformedProcedureStepSequence = refd_performed_procedure_step_sequence

    # Referenced Performed Procedure Step Sequence: Referenced Performed Procedure Step 1
    refd_performed_procedure_step1 = Dataset()
    refd_performed_procedure_step1.ReferencedSOPClassUID = '1.2.840.10008.3.1.2.3.3'
    refd_performed_procedure_step1.ReferencedSOPInstanceUID = '1.2.840.113704.1.111.5104.1160636572.51'
    refd_performed_procedure_step_sequence.append(refd_performed_procedure_step1)

    ds.PatientName = 'Anonymized'
    ds.PatientID = str(pid)
    ds.PatientAge = '000Y'
    ds.ContrastBolusAgent = 'CONTRAST'
    ds.ScanOptions = 'HELIX'
    ds.SliceThickness = "1.0"
    ds.KVP = "120.0"
    ds.SpacingBetweenSlices = "0.5"
    ds.DataCollectionDiameter = "302.0"
    ds.ProtocolName = 'ART.RENALES 12/Abdomen/Hx'
    ds.ReconstructionDiameter = "302.0"
    ds.GantryDetectorTilt = "0.0"
    ds.TableHeight = "151.0"
    ds.RotationDirection = 'CW'
    ds.XRayTubeCurrent = "400"
    ds.Exposure = "300"
    ds.FilterType = 'B'
    ds.ConvolutionKernel = 'B'
    ds.PatientPosition = 'FFS'
    ds.StudyInstanceUID = '1.2.826.0.1.3680043.8.1055.1.{}.92402465.76095170'.format(date)
    ds.SeriesInstanceUID = '1.2.826.0.1.3680043.8.1055.1.{}.96842950.07877442'.format(date)
    ds.SeriesNumber = "6168"
    ds.InstanceNumber = str(innumber)
    ds.ImagePositionPatient = [-151.493508, -36.6564417, 1295]
    ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
    ds.FrameOfReferenceUID = '1.2.840.113704.1.111.3704.{}.3'.format(date)
    ds.SliceLocation = "-325.0"
    ds.ImageComments = 'JPEG 2000 lossless - Version 4.0.2 (c) Image Devices GmbH'
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = 'MONOCHROME2'
    ds.Rows = row
    ds.Columns = column
    ds.PixelSpacing = [0.58984375, 0.58984375]
    ds.BitsAllocated = 16
    ds.BitsStored = 12
    ds.HighBit = 11
    ds.PixelRepresentation = 0
    ds.WindowCenter = [00050, 00050]
    ds.WindowWidth = [00350, 00350]
    ds.RescaleIntercept = "-1000.0"
    ds.RescaleSlope = "1.0"
    ds.LossyImageCompression = '01'
    ds.LossyImageCompressionRatio = "5.88268"
    ds.ScheduledProcedureStepDescription = 'CT1 abdomen'

    # Scheduled Protocol Code Sequence
    scheduled_protocol_code_sequence = Sequence()
    ds.ScheduledProtocolCodeSequence = scheduled_protocol_code_sequence

    # Scheduled Protocol Code Sequence: Scheduled Protocol Code 1
    scheduled_protocol_code1 = Dataset()
    scheduled_protocol_code1.CodeValue = 'CTABDOM'
    scheduled_protocol_code1.CodingSchemeDesignator = 'XPLORE'
    scheduled_protocol_code1.CodeMeaning = 'CT1 abdomen'
    scheduled_protocol_code_sequence.append(scheduled_protocol_code1)

    ds.ScheduledProcedureStepID = 'A10026177758'
    ds.PerformedProcedureStepDescription = 'CT1 abdomen'

    # Performed Protocol Code Sequence
    performed_protocol_code_sequence = Sequence()
    ds.PerformedProtocolCodeSequence = performed_protocol_code_sequence

    # Performed Protocol Code Sequence: Performed Protocol Code 1
    performed_protocol_code1 = Dataset()
    performed_protocol_code1.CodeValue = 'CTABDOM'
    performed_protocol_code1.CodingSchemeDesignator = 'XPLORE'
    performed_protocol_code1.CodeMeaning = 'CT1 abdomen'
    performed_protocol_code_sequence.append(performed_protocol_code1)


    # Request Attributes Sequence
    request_attributes_sequence = Sequence()
    ds.RequestAttributesSequence = request_attributes_sequence

    # Request Attributes Sequence: Request Attributes 1
    request_attributes1 = Dataset()
    request_attributes1.ScheduledProcedureStepDescription = 'CT1 abdomen'

    # Scheduled Protocol Code Sequence
    scheduled_protocol_code_sequence = Sequence()
    request_attributes1.ScheduledProtocolCodeSequence = scheduled_protocol_code_sequence

    # Scheduled Protocol Code Sequence: Scheduled Protocol Code 1
    scheduled_protocol_code1 = Dataset()
    scheduled_protocol_code1.CodeValue = 'CTABDOM'
    scheduled_protocol_code1.CodingSchemeDesignator = 'XPLORE'
    scheduled_protocol_code1.CodeMeaning = 'CT1 abdomen'
    scheduled_protocol_code_sequence.append(scheduled_protocol_code1)

    request_attributes1.ScheduledProcedureStepID = 'A10026177758'
    request_attributes1.RequestedProcedureID = 'A10026177757'
    request_attributes_sequence.append(request_attributes1)

    ds.RequestedProcedureID = 'A10026177757'
    # ds.PixelData = # XXX Array of 89144 bytes excluded
    ds.PixelData = data

    ds.file_meta = file_meta
    ds.is_implicit_VR = False
    ds.is_little_endian = True
    ds.save_as(outputfile, write_like_original=False)
    print(outputfile+'保存成功')