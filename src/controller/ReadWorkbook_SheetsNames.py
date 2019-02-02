'''
    This file lists the names of the sheets in the default WaMDaM workbook template 
    It also lists the Controlled Vocabulary tables in the online repository of
    http://vocabulary.wamdam.org/
    
    It is helpful and used to to check any provided workbook against the list of 
    these sheet names, if the provided workbook is missing any of these sheet names,
    then it does not comply with the Wizard and an error msg is raised.

'''

from model.SqlAlchemy import *

from collections import OrderedDict


# Creating a dictionary to map CV tables to the
# online repository of Controlled Vocabulary http://vocabulary.wamdam.org/
# key, value
vocab = OrderedDict({
    "aggregationstatistic": CV_AggregationStatistic,
    "attributedatatype": CV_AttributeDataType,
    "attributename": CV_AttributeName,
    "electronicfileformat": CV_ElectronicFileFormat,
    "instancename": CV_InstanceName,
    "methodtype": CV_MethodType,
    "resourcetype": CV_ResourceType,
    "objecttypology": CV_ObjectTypology,
    "objecttype": CV_ObjectType,
    "seasonname": CV_SeasonName,
    "spatialreference": CV_SpatialReference,
    "categorical": CV_Categorical,
    "units": CV_Units,
    "elevationdatum": CV_ElevationDatum
})


# Sheet Names for step 1 loading in order of dependency, independent to dependent. (Metadata)
metadata_sheets_ordered = ['1.1_Organiz&People', '1.2_Sources&Methods']


# Sheet Names for loading structure data in order of dependency (structure)
struct_sheets_ordered = ['ObjectCategory', 'AttributeCategory', '2.1_ResourceTypes&ObjectTypes',
                         '2.2_Attributes']


# Sheet Names for step 3 loading in order (Networks)
Network_sheets_ordered = ['InstanceCategory', '3.1_Networks&Scenarios', '3.2_Nodes', '3.3_Links']


# Sheet Names for step 4 loading in order (Datavalues)
datavalues_sheets_ordered = ['4_NumericValues', '4_SeasonalNumericValues', '4_TimeSeries',
                             '4_CategoricalValues', '4_TimeSeriesValues', '4_ElectronicFiles', '4_MultiAttributeSeries',
                             '4_FreeText']


row_start_data_values = {'4_MultiAttributeSeries': 14}
