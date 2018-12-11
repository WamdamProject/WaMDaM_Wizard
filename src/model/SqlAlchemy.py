#!/usr/bin/env python
# -*- coding: utf-8 -*-#

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine, BLOB, Date, Text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import warnings
from sqlalchemy.exc import SAWarning
from sqlalchemy.pool import NullPool

#[[say what this one does,  ]]
warnings.filterwarnings('ignore',
                        r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
                        "and SQLAlchemy must convert from floating point - rounding errors and other "
                        "issues may occur\. Please consider storing Decimal numbers as strings or "
                        "integers on this platform for lossless storage\.$",
                        SAWarning, r'^sqlalchemy\.sql\.type_api$')

Base = declarative_base()

sessionmaker(autoflush=True)
__engine = create_engine('sqlite:///Data/wdm.sqlite')
__session = None


def connect(dbpath, db_type, sql_string=None):
    if db_type == 'mysql':
        # used to create and connect to a mysql database.
        mysql_conn = 'mysql+mysqldb://' + sql_string
        __engine = create_engine(mysql_conn, pool_recycle=3600)
        __engine.String_factor = lambda x: unicode(x, "utf-8", "ignore")

    else:
        # used to create and connect to a mysqlite database.
        sqlite_conn = "sqlite:///" + dbpath.replace('\\', '//')
        __engine = create_engine(sqlite_conn, connect_args={'check_same_thread': False}, poolclass=NullPool, encoding='unicode_escape')
        __engine.String_factor = lambda x: unicode(x, "utf-8", "ignore")

    # if db has nothing in it call SqlAlchemy.init(__engine)
    if len(__engine.table_names()) == 0:
        print '*****************'
        #[[Add this comment to the logfile]]
        print 'creating tables'
        print '*****************'
        init(__engine)
        init(__engine)
    __session = sessionmaker(bind=__engine)()
    return __session


def init(engine = None):
    if engine:
        metadata = Base.metadata.create_all(engine)
    else:
        metadata = Base.metadata.create_all(__engine)


def get_session():
    return __session


# ****************************************************************************************************************** #
#                                                                                                                    #
#                                           CREATE CV TABLES                                                         #
#                                                                                                                    #
# ****************************************************************************************************************** #


class WaMDaMVersion(Base):
    __tablename__ = 'WaMDaMVersion'
    VersionNumber = Column(Float, primary_key=True)


class CV_AggregationStatistic(Base):
    __tablename__ = 'CV_AggregationStatistic'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), nullable=False)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_AttributeDataType(Base):
    __tablename__ = 'CV_AttributeDataType'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_AttributeName(Base):
    __tablename__ = 'CV_AttributeName'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_ResourceType(Base):
    __tablename__ = 'CV_ResourceType'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_ElectronicFileFormat(Base):
    __tablename__ = 'CV_ElectronicFileFormat'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_InstanceName(Base):
    __tablename__ = 'CV_InstanceName'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))

class CV_MethodType(Base):
    __tablename__ = 'CV_MethodType'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_ObjectTypology(Base):
    __tablename__ = 'CV_ObjectTypology'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_ObjectType(Base):
    __tablename__ = 'CV_ObjectType'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_SeasonName(Base):
    __tablename__ = 'CV_SeasonName'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_SpatialReference(Base):
    __tablename__ = 'CV_SpatialReference'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_Categorical(Base):
    __tablename__ = 'CV_Categorical'

    Name = Column(String(255), primary_key=False)
    Term = Column(String(255), primary_key=True)
    AttributeName = Column(String(255)) # Column(ForeignKey('CV_AttributeName.Name'))
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))


class CV_Units(Base):
    __tablename__ = 'CV_Units'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), primary_key=True)
    Definition = Column(String(5000))
    Category = Column(String(255), nullable=False)
    UnitAbbreviation = Column(String(50))
    UnitSystem = Column(String(255))# Metric or English
    LinearFactor = Column(Float)
    ConstantFactor = Column(Float)
    SourceVocabularyURI = Column(String(255))


class CV_ElevationDatum(Base):
    __tablename__ = 'CV_ElevationDatum'

    Name = Column(String(255), primary_key=True)
    Term = Column(String(255), nullable=False)
    Definition = Column(String(5000))
    Category = Column(String(255))
    SourceVocabularyURI = Column(String(255))



# ****************************************************************************************************************** #
#                                                                                                                    #
#                                           CREATE DATASTRUCTURE TABLES                                              #
#                                                                                                                    #
# ****************************************************************************************************************** #


class AttributeCategories(Base):
    __tablename__ = 'AttributeCategories'

    AttributeCategoryID = Column(Integer, primary_key=True)
    AttributeCategoryName = Column(String(255), nullable=False)
    CategoryDefinition = Column(Text)


class Attributes(Base):
    __tablename__ = 'Attributes'

    AttributeID = Column(Integer, primary_key=True)
    AttributeName = Column(String(255), nullable=False)
    AttributeName_Abstract = Column(String(255))
    AttributeNameCV = Column(ForeignKey('CV_AttributeName.Name'))
    ObjectTypeID = Column(ForeignKey('ObjectTypes.ObjectTypeID'), nullable=False)
    UnitNameCV = Column(ForeignKey('CV_Units.Name'))
    UnitName = Column(String(255))
    AttributeDataTypeCV = Column(ForeignKey('CV_AttributeDataType.Name'), nullable=False)
    AttributeCategoryID = Column(ForeignKey('AttributeCategories.AttributeCategoryID'))
    ModelInputOrOutput = Column(String(50))
    Description = Column(Text)
    AttributeScale = Column(Integer)

    ObjectTypes = relationship('ObjectTypes')
    Units = relationship('CV_Units')
    AttributeDataTypes = relationship('CV_AttributeDataType')
    AttributeCategories = relationship('AttributeCategories')
    AttributeNames = relationship('CV_AttributeName')


class ResourceTypes(Base):
    __tablename__ = 'ResourceTypes'

    ResourceTypeID = Column(Integer, primary_key=True)
    ResourceType = Column(String(255), nullable=False)
    ResourceTypeAcronym = Column(String(255), nullable=False)
    ResourceTypeCV = Column(ForeignKey('CV_ResourceType.Name'))
    MethodID = Column(ForeignKey('Methods.MethodID'), nullable=False)
    Description = Column(Text)

    Methods = relationship('Methods')
    CV_ResourceType = relationship('CV_ResourceType')


class ObjectCategories(Base):
    __tablename__ = 'ObjectCategories'

    ObjectCategoryID = Column(Integer, primary_key=True)
    ObjectCategoryName = Column(String(255), nullable=False)
    CategoryDefinition = Column(Text)


class ObjectTypes(Base):
    __tablename__ = 'ObjectTypes'

    ObjectTypeID = Column(Integer, primary_key=True)
    ObjectType = Column(String(255), nullable=False)
    ObjectTypeCV = Column(ForeignKey('CV_ObjectType.Name'))
    ObjectTypologyCV = Column(ForeignKey('CV_ObjectTypology.Name'), nullable=False)
    Layout = Column(String(1000))
    Description = Column(Text)
    ObjectCategoryID = Column(ForeignKey('ObjectCategories.ObjectCategoryID'))
    ResourceTypeID = Column(ForeignKey('ResourceTypes.ResourceTypeID'), nullable=False)

    ResourceTypes = relationship('ResourceTypes')
    ObjectCategories = relationship('ObjectCategories')
    ObjectTypes = relationship('CV_ObjectType')
    ObjectTypology = relationship('CV_ObjectTypology')



# ****************************************************************************************************************** #
#                                                                                                                    #
#                                           CREATE DATAVALUE TABLES                                                  #
#                                                                                                                    #
# ****************************************************************************************************************** #




class ValuesMapper(Base):
    __tablename__ = 'ValuesMapper'

    ValuesMapperID = Column(Integer, primary_key=True)


class ElectronicFiles(Base):
    __tablename__ = 'ElectronicFiles'

    ElectronicFileID = Column(Integer, primary_key=True)
    ElectronicFileName = Column(String(255), nullable=False)
    ElectronicFile = Column(BLOB, nullable=False)
    ElectronicFileFormatCV = Column(ForeignKey('CV_ElectronicFileFormat.Name'))
    Description = Column(Text)
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)

    ValuesMapper = relationship('ValuesMapper')
    ElectronicFileFormat = relationship('CV_ElectronicFileFormat')


class MultiAttributeSeries(Base):
    __tablename__ = 'MultiAttributeSeries'

    MultiAttributeSeriesID = Column(Integer, primary_key=True)
    MappingID_Attribute = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)

    # MultiAttributeSeries = relationship('MappingID_Attribute')
    # ValuesMapper = relationship('ValuesMapper')

    ValuesMapper = relationship('ValuesMapper',
                                    primaryjoin='MultiAttributeSeries.MappingID_Attribute == ValuesMapper.ValuesMapperID')
    ValuesMapper1 = relationship('ValuesMapper',
                                     primaryjoin='MultiAttributeSeries.ValuesMapperID == ValuesMapper.ValuesMapperID')


class MultiAttributeSeriesValues(Base):
    __tablename__ = 'MultiAttributeSeriesValues'

    MultiAttributeSeriesValueID = Column(Integer, primary_key=True)
    DataValue = Column(String(255), nullable=False)
    ValueOrder = Column(Integer, nullable=False)
    MultiAttributeSeriesID = Column(ForeignKey('MultiAttributeSeries.MultiAttributeSeriesID'), nullable=False)

    MultiAttributeSeries = relationship('MultiAttributeSeries')


class NumericValues(Base):
    __tablename__ = 'NumericValues'

    NumericValueID = Column(Integer, primary_key=True)
    NumericValue = Column(Float, nullable=False)
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)

    ValuesMapper = relationship('ValuesMapper')


class SeasonalNumericValues(Base):
    __tablename__ = 'SeasonalNumericValues'

    SeasonalNumericValueID = Column(Integer, primary_key=True)
    SeasonName = Column(String(255))
    SeasonDateFormate=Column(Date)
    SeasonNameCV = Column(ForeignKey('CV_SeasonName.Name'))
    SeasonOrder = Column(Integer)
    SeasonNumericValue = Column(String(500), nullable=False)
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)

    ValuesMapper = relationship('ValuesMapper')
    SeasonNames = relationship('CV_SeasonName')


class CategoricalValues(Base):
    __tablename__ = 'CategoricalValues'

    CategoricalValueID = Column(Integer, primary_key=True)
    CategoricalValue = Column(String(500), nullable=False)
    CategoricalValueCV = Column(ForeignKey('CV_Categorical.Name'))
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)

    ValuesMapper = relationship('ValuesMapper')
    CategoricalValues = relationship('CV_Categorical')



class FreeText(Base):
    __tablename__ = 'FreeText'

    FreeTextID = Column(Integer, primary_key=True)
    FreeTextValue = Column(Text, nullable=False)
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)

    ValuesMapper = relationship('ValuesMapper')



class TimeSeries(Base):
    __tablename__ = 'TimeSeries'

    TimeSeriesID = Column(Integer, primary_key=True)
    YearType = Column(String(50), nullable=False)
    AggregationStatisticCV = Column(ForeignKey('CV_AggregationStatistic.Name'), nullable=False)
    AggregationInterval = Column(Float, nullable=False)
    IntervalTimeUnitCV = Column(ForeignKey('CV_Units.Name'), nullable=False)
    BeginDateTime = Column(DateTime)
    EndDateTime = Column(DateTime)
    IsRegular = Column(Integer)
    NoDataValue = Column(String(50))
    Description = Column(Text)
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'), nullable=False)

    AggregationStatistic = relationship('CV_AggregationStatistic')
    ValuesMapper = relationship('ValuesMapper')
    Units = relationship('CV_Units')


class TimeSeriesValues(Base):
    __tablename__ = 'TimeSeriesValues'

    TimeSeriesValueID = Column(Integer, primary_key=True)
    TimeSeriesID = Column(ForeignKey('TimeSeries.TimeSeriesID'), nullable=False)
    DateTimeStamp = Column(Date, nullable=False)
    DataValue = Column(Float, nullable=False)

    TimeSeries = relationship('TimeSeries')





# ****************************************************************************************************************** #
#                                                                                                                    #
#                                            CREATE METADATA TABLES                                                  #
#                                                                                                                    #
# ****************************************************************************************************************** #


class Methods(Base):
    __tablename__ = 'Methods'

    MethodID = Column(Integer, primary_key=True)
    MethodName = Column(String(255), nullable=False)
    MethodWebpage = Column(String(255))
    MethodCitation = Column(String(500))
    MethodTypeCV = Column(ForeignKey('CV_MethodType.Name'))
    PersonID = Column(ForeignKey('People.PersonID'), nullable=False)
    Description = Column(Text)
    DataQuality=Column(Text)

    MethodType = relationship('CV_MethodType')
    People = relationship('People')


class Organizations(Base):
    __tablename__ = 'Organizations'

    OrganizationID = Column(Integer, primary_key=True)
    OrganizationName = Column(String(255), nullable=False)
    OrganizationType = Column(String(255))
    OrganizationWebpage = Column(String(255))
    Description = Column(Text)


class People(Base):
    __tablename__ = 'People'

    PersonID = Column(Integer, primary_key=True)
    PersonName = Column(String(255), nullable=False)
    Address = Column(String(255))
    Email = Column(String(255))
    Phone = Column(String(50))
    PersonWebpage = Column(String(255))
    Position = Column(String(255))
    OrganizationID = Column(ForeignKey('Organizations.OrganizationID'), nullable=False)

    Organizations = relationship('Organizations')


class Sources(Base):
    __tablename__ = 'Sources'

    SourceID = Column(Integer, primary_key=True)
    SourceName = Column(String(500), nullable=False)
    SourceWebpage = Column(String(500))
    SourceCitation = Column(String(500))
    PersonID = Column(ForeignKey('People.PersonID'), nullable=False)
    Description = Column(Text)

    People = relationship('People')



# ****************************************************************************************************************** #
#                                                                                                                    #
#                                            CREATE METADATA TABLES                                                  #
#                                                                                                                    #
# ****************************************************************************************************************** #


class Connections(Base):
    __tablename__ = 'Connections'

    ConnectivityID = Column(Integer, primary_key=True)
    LinkInstanceID = Column(ForeignKey('Instances.InstanceID'), nullable=False)
    StartNodeInstanceID = Column(ForeignKey('Instances.InstanceID'), nullable=False)
    EndNodeInstanceID = Column(ForeignKey('Instances.InstanceID'), nullable=False)

    Instance = relationship('Instances', primaryjoin='Connections.EndNodeInstanceID == Instances.InstanceID')
    Instance1 = relationship('Instances', primaryjoin='Connections.LinkInstanceID == Instances.InstanceID')
    Instance2 = relationship('Instances', primaryjoin='Connections.StartNodeInstanceID == Instances.InstanceID')


class InstanceCategories(Base):
    __tablename__ = 'InstanceCategories'

    InstanceCategoryID = Column(Integer, primary_key=True)
    InstanceCategory = Column(String(255), nullable=False)
    CategoryDefinition = Column(Text)


class Instances(Base):
    __tablename__ = 'Instances'

    InstanceID = Column(Integer, primary_key=True)
    InstanceName = Column(String(255), nullable=False)
    InstanceNameCV = Column(ForeignKey('CV_InstanceName.Name'))
    Longitude_x = Column(Float)
    Latitude_y = Column(Float)
    Description = Column(Text)
    InstanceCategoryID = Column(ForeignKey('InstanceCategories.InstanceCategoryID'))

    InstanceNames = relationship('CV_InstanceName')
    InstanceCategories = relationship('InstanceCategories')


class Mappings(Base):
    __tablename__ = 'Mappings'

    MappingID = Column(Integer, primary_key=True)
    AttributeID = Column(ForeignKey('Attributes.AttributeID'), nullable=False)
    InstanceID = Column(ForeignKey('Instances.InstanceID'), nullable=False)
    SourceID = Column(ForeignKey('Sources.SourceID'), nullable=False)
    MethodID = Column(ForeignKey('Methods.MethodID'), nullable=False)
    ValuesMapperID = Column(ForeignKey('ValuesMapper.ValuesMapperID'))
    Verified = Column(String(5))


    ValuesMapper = relationship('ValuesMapper')
    Instances = relationship('Instances')
    Methods = relationship('Methods')
    Attributes = relationship('Attributes')
    Sources = relationship('Sources')


class MasterNetworks(Base):
    __tablename__ = 'MasterNetworks'

    MasterNetworkID = Column(Integer, primary_key=True)
    MasterNetworkName = Column(String(255), nullable=False)
    SpatialReferenceNameCV = Column(ForeignKey('CV_SpatialReference.Name'))
    VerticalDatumCV = Column(ForeignKey('CV_ElevationDatum.Name'))
    Description = Column(Text)

    SpatialReference = relationship('CV_SpatialReference')
    VerticalDatum = relationship('CV_ElevationDatum')


class ScenarioMappings(Base):
    __tablename__ = 'ScenarioMappings'

    ScenarioMappingID = Column(Integer, primary_key=True)
    ScenarioID = Column(ForeignKey('Scenarios.ScenarioID'), nullable=False)
    MappingID = Column(ForeignKey('Mappings.MappingID'), nullable=False)

    Mappings = relationship('Mappings')
    Scenarios = relationship('Scenarios')


class Scenarios(Base):
    __tablename__ = 'Scenarios'

    ScenarioID = Column(Integer, primary_key=True)
    ScenarioName = Column(String(255), nullable=False)
    ScenarioStartDate = Column(Date)
    ScenarioEndDate = Column(Date)
    TimeStepValue = Column(Integer)
    TimeStepUnitCV = Column(ForeignKey('CV_Units.Name'))
    MasterNetworkID = Column(ForeignKey('MasterNetworks.MasterNetworkID'), nullable=False)
    Description = Column(Text)

    MasterNetworks = relationship('MasterNetworks')
    Units = relationship('CV_Units')


