# stp2_loadDataStructure.py
'''
    The load_step_2.py file is used to load structure data.
    to the sqlite database using sqlalchemy.
    It Inherits properties from the Parse_Excel_File and DB_Setup
    classes.
    It is primarily made up of:
    - Load_Struct_To_DB():  This is the class for loading Structure data in this
                            file. It inherits methods for two other classes so as
                            to achieve its task. This class is made up of a
                            constructor used to initialize its self and its
                            inherited classes, setup the session which is a
                            private variable and also initialize the work_sheet
                            variable which holds all data from sheets in the
                            excel files.
        Important methods and variables of the class:
        -> load_data(): This is a method which does all the processing of each Structure data.
                        it functions by iterating through the work_sheet dictionary, and
                        for each sheet parse the data appropriately so as to store in the
                        required table and fields.
        -> work_sheet:  This a dictionary having structure sheet data as keys and the sheet
                        data as values. its data is gotten from the
                        parse_object_control_value() method found in Parse_Excel_File class.
        -> __session:   Session variables (private) used to access the database.
'''
# We import required variables (this are the metadata sheet names and their start values in the excel file)

from .ReadWorkbook_SheetsNames import struct_sheets_ordered
from sqlalchemy import and_
# We Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by Load_CV_To_DB and Load_Struct_To_DB clases
from .ConnectDB_ParseExcel import *
import define

# ****************************************************************************************************************** #
#                                                                                                                    #
#                                    Script Begins here for loading Structure Data                                   #
#                                                                                                                    #
# ****************************************************************************************************************** #


class Load_Struct_To_DB(Parse_Excel_File):
    """
        Class used to load Structure data to database
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the class constructor used to initialize inherited
        clases and some variables
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(Load_Struct_To_DB, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value(struct_sheets_ordered)
        self.datasetAcronym = ''
    def create_dummy_attrib(self, dum_attrib):
        """
        This method creates dummy record in the attribute table when loading
        datasets and objecttypes. Also contributes in creating links in the
        database
        :param dum_attrib: Dummy attribute name
        :return: An instance of the Attributes() table
        """
        # crating dummy attribute record for dummy object type records
        dummy_attrib = SqlAlchemy.Attributes()
        if not isinstance(dum_attrib[0], int):
            dummy_attrib.AttributeName = dum_attrib[0]
            dummy_attrib.ObjectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).order_by(
                SqlAlchemy.ObjectTypes.ObjectTypeID.desc()).first().ObjectTypeID
        else:
            dummy_attrib.AttributeName = 'DatasetAcronym'
            dummy_attrib.ObjectTypeID = dum_attrib[0]

        dummy_attrib.UnitNameCV = self.__session.query(SqlAlchemy.CV_Units).filter(
            SqlAlchemy.CV_Units.Name == 'Dimensionless'
        ).first().Name

        dummy_attrib.AttributeDataTypeCV = self.__session.query(SqlAlchemy.CV_AttributeDataType).filter(
            SqlAlchemy.CV_AttributeDataType.Name == 'Dummy'
        ).first().Name

        dummy_attrib.AttributeNameCV = None

        dummy_attrib.AttributeCategoryID = None

        dummy_attrib.ModelInputOrOutput = None
        dummy_attrib.AttributeDescription = dum_attrib[1]
        return dummy_attrib

    def load_data(self, sheet_names):
        """
            This method is used to parse data from each sheet to its
            appropriate table in the database.
            Due to the structure of the excel file, some hard coding
            was done to get data accurately.
            It functions by iterating over the work_sheet dictionary
            and getting each corresponding sheet_name and sheetrows,
            then using if statements to test what sheet it is , afterwards
            the appropriate table is initialized and the table fields are
            loaded using data from the corresponding sheet.
            Some dummy Data (objecttypes and attributes) are also loaded
            accordingly when loading datasets and objecttypes.
            :param sheet_names:
            :return: None
        """
        # print self.work_sheet

        static_rownum = 10
        for sheet_name, sheet_rows in self.work_sheet.items():
            dataset_acronyms = list()
            temp = sheet_rows[:]
            for row_id, row in enumerate(temp):
                temp_row = [cell.value for cell in row]

                if sheet_name == sheet_names[0]:
                    if 'ObjectCategory_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum - 2
                            if all('' == cell.value for cell in row):
                                break
                            obj_cat = SqlAlchemy.ObjectCategory()
                            if row[0].value == "":
                                raise Exception('Error in {} row of "ObjectCategory_table" of sheet {}\nField named "ObjectCategoryName" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[0]))
                            obj_cat.ObjectCategoryName = row[0].value
                            obj_cat.CategoryDefinition = row[1].value
                            self.setup.push_data(obj_cat)
                        break

                if sheet_name == sheet_names[1]:
                    if 'AttributeCategory_table' in temp_row:
                        cur_table = sheet_rows[row_id + 3:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum - 3

                            if all('' == cell.value for cell in row):
                                break
                            attrib_cat = SqlAlchemy.AttributeCategory()
                            if row[0].value == "":
                                raise Exception('Error in {} row of "AttributeCategory_table" of sheet "{}"\nField named "AttributeCategoryName" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[1]))
                            attrib_cat.AttributeCategoryName = row[0].value
                            attrib_cat.CategoryDefinition = row[1].value
                            self.setup.push_data(attrib_cat)
                        break

                if sheet_name == sheet_names[2]:
                    temp_row = [cell.value for cell in row]
                    if 'Datasets_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        temp_org = cur_table[:]
                        for row_id, row in enumerate(cur_table):
                            temp_row = [cell.value for cell in row]
                            row_id = row_id + static_rownum
                            if all('' == cell.value for cell in row):
                                break
                            data_struct = SqlAlchemy.Datasets()

                            if row[0].value == "":
                                raise Exception('Error in {} row of "Datasets_table" of sheet "{}"\nField named "DatasetName" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[2]))
                            if row[1].value == "":
                                raise Exception('Error in {} row of "Datasets_table" of sheet "{}"\nField named "DatasetAcronym" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[2]))

                            if row[2].value == "":
                                raise Exception('Error in {} row of "Datasets_table" of sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[2]))

                            if not row[0].value:


                                raise Exception('Error in "Datasets_table" of sheet "{}"\nField named "DatasetName" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(sheet_names[2]))
                                # raise Exception('Empty Field found in DatasetName Column in Dataset table')
                            existname = self.__session.query(SqlAlchemy.Datasets).filter(
                                    SqlAlchemy.Datasets.DatasetName == row[0].value
                                ).first()
                            if existname == None:
                                data_struct.DatasetName = row[0].value
                                if row[1].value:
                                    data_struct.DatasetAcronym = row[1].value
                                    self.datasetAcronym = row[1].value
                                    define.datasetName = row[1].value
                                else:
                                    raise Exception('Error in "Datasets_table" of sheet "{}"\nField named "DatasetAcronym" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                    .format(sheet_names[2]))
                                    # raise Exception('Empty Fields found in DatasetAcronym Column in Dataset table')

                                try:
                                    data_struct.SourceID = self.__session.query(SqlAlchemy.Sources).filter(
                                        SqlAlchemy.Sources.SourceName == row[2].value
                                    ).first().SourceID
                                except Exception as e:
                                    print e
                                    raise Exception('Error in sheet {}\ncould not find {} in Sources\n\n'
                                                    .format(sheet_names[2], row[2].value))
                                data_struct.Description = row[3].value
                                self.setup.push_data(data_struct)

                                # Storing DatasetAcronym in Dict.
                                if not row[1].value in dataset_acronyms:
                                    dataset_acronyms.append(row[1].value)

                    if 'ObjectTypes_table' in temp_row:
                        cur_table = sheet_rows[row_id + 5:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum + 8
                            if all('' == cell.value for cell in row):
                                break
                            # Loading main ObjectTypes into the database
                            obj_type = SqlAlchemy.ObjectTypes()

                            # Raise an error if the user leaves the required field "ObjectType" empty
                            if row[0].value == '':
                                raise Exception('Error in ObjectTypes_table\'s {} row of sheet {}\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[2], row[0].value))

                            # Raise an error if the user leaves the required field "ObjectTypology" empty
                            if row[1].value == '':
                                raise Exception('Error in {} row of "ObjectTypes_table" of sheet {}\nField named "ObjectTypology"  which "ObjectType" is {} is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[2], row[0].value))
                            # Raise an error if the user leaves the required field "DatasetAcronym" empty
                            if row[2].value == '':
                                raise Exception('Error in {} row of "ObjectTypes_table" of sheet {}\n"DatasetAcronym" field which "ObjectType" is  {} is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[2],row[0].value))

                            obj_type.ObjectType = row[0].value
                            obj_type.ObjectTypologyCV = row[1].value

                            try:
                                if row[2].value:
                                    obj_type.DatasetID = self.__session.query(SqlAlchemy.Datasets).filter(
                                        SqlAlchemy.Datasets.DatasetAcronym == row[2].value
                                    ).first().DatasetID
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\ncould not find {} in Datasets\n\n'
                                                .format(sheet_names[2], row[2].value))

                            try:
                                if row[3].value:
                                    obj_type.ObjectTypeCV = self.__session.query(SqlAlchemy.CV_ObjectType).filter(
                                        SqlAlchemy.CV_ObjectType.Name == row[3].value
                                    ).first().Name
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\ncould not find {} in ObjectTypeCV\n\n'
                                                .format(sheet_names[2], row[3].value))

                            try:
                                if row[6].value:
                                    obj_type.ObjectCategoryID = self.__session.query(SqlAlchemy.ObjectCategory).filter(
                                        SqlAlchemy.ObjectCategory.ObjectCategoryName == row[6].value
                                    ).first().ObjectCategoryID
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\ncould not find {} in ObjectCategory\n\n'
                                                .format(sheet_names[2], row[6].value))

                            if row[7]:
                                obj_type.Description = row[7].value

                            self.setup.push_data(obj_type)
                            # Creating dummy attributes for corresponding object type
                            obj = self.create_dummy_attrib(['ObjectTypeInstances', "The purpose of this "
                                                                                        "Attribute is to connect"
                                                                                        " and help query all "
                                                                                        "the instances that "
                                                                                        "belong to one "
                                                                                        "ObjectType"])
                            self.setup.push_data(obj)

                        # Code fragment to create dummy attributes when dataset is loaded. [[delete this stuff??]]

                        # for dataAcronym in dataset_acronyms:
                        #     object_id = self.__session.query(sq.ObjectTypes).filter(
                        #         sq.ObjectTypes.ObjectType == dataAcronym
                        #     ).first().ObjectTypeID
                        #     obj = self.create_dummy_attrib([int(object_id), 'The purpose of this Attribute is '
                        #                                                     'to connect and help query a '
                        #                                                     'scenario and network for a '
                        #                                                     'dataset.'])
                        #     self.push_data(obj)
                        # self.add_data()
                        break

                if sheet_name == sheet_names[3]:
                    if 'Attributes_table' in temp_row:
                        cur_table = sheet_rows[row_id + 5:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum
                            if all('' == cell.value for cell in row):
                                break
                            #print row
                            attrib = SqlAlchemy.Attributes()
                            if row[0].value == "":
                                raise Exception('Error in {} row of "Attributes_table" of sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[3]))

                            if row[1].value == "":
                                raise Exception('Error in {} row of "Attributes_table" of sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[3]))

                            if row[3].value == "":
                                raise Exception('Error in {} row of "Attributes_table" of sheet "{}"\nField named "AttributeUnit" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[3]))

                            if row[5].value == "":
                                raise Exception('Error in {} row of "Attributes_table" of sheet "{}"\nField named "AttributeDataTypeCV" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(row_id, sheet_names[3]))

                            if row[1].value:
                                attrib.AttributeName = row[1].value
                            else:
                                raise Exception('Error in "Attributes_table" of sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value\n\n'
                                                .format(sheet_names[3]))
                                # raise Exception('Empty field found in AttributeName \n\n Column of Attributes table')
                            try:
                                if row[0]:
                                    try:
                                        DatasetID = self.__session.query(SqlAlchemy.Datasets).filter(
                                            SqlAlchemy.Datasets.DatasetAcronym == self.datasetAcronym
                                        ).first().DatasetID
                                        attrib.ObjectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                            and_(
                                                SqlAlchemy.ObjectTypes.ObjectType == row[0].value,
                                                SqlAlchemy.ObjectTypes.DatasetID == DatasetID
                                            )
                                        ).first().ObjectTypeID
                                    except Exception as e:
                                        print e
                                        raise Exception(e.message)
                                else:
                                    raise Exception('Empty field found in ObjectType Column of Attributes table \n\n')
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\n could not find {} in ObjectTypes\n\n'
                                                .format(sheet_names[3], row[0].value))

                            if row[2].value:
                                attrib.AttributeNameCV = row[2].value

                            # if row[2].value:
                            #     attrib.UnitName = row[3].value
                            # else:
                            #     raise Exception('Empty field found in AttributeUnit column of Attributes sheet')

                            if row[4].value:
                                try:
                                    attrib.UnitNameCV = self.__session.query(SqlAlchemy.CV_Units).filter(
                                            SqlAlchemy.CV_Units.Name == row[4].value
                                        ).first().Name
                                except Exception as e:
                                    print e
                                    raise Exception("Error in sheet '{}'\n could not find '{}' in CV_Units table\n\n"
                                                    .format(sheet_names[3], row[2].value))

                            if row[3].value:
                                attrib.UnitName = row[3].value
                                # try:
                                #     attrib.UnitName = self.__session.query(SqlAlchemy.CV_Units).filter(
                                #         SqlAlchemy.CV_Units.Name == row[3].value
                                #     ).first().Name
                                # except Exception as e:
                                #     print e
                                #     raise Exception('Error in sheet {}\ncould not find {} in AttributeTypes\n\n'
                                #                     .format(sheet_names[3], row[3].value))
                            else:
                                raise Exception('Error in "Attributes_table" of sheet "{}"\nField named "AttributeUnit" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(sheet_names[3]))
                                # raise Exception('Empty field found in AttributeDataTypeCV column of Attributes table')
                            if row[5].value:
                                try:
                                    attrib.AttributeDataTypeCV = self.__session.query(SqlAlchemy.CV_AttributeDataType).filter(
                                        SqlAlchemy.CV_AttributeDataType.Name == row[5].value
                                    ).first().Name
                                except Exception as e:
                                    print e
                                    raise Exception('Error in sheet {}\ncould not find {} in AttributeDataTypeCV\n\n'
                                                    .format(sheet_names[3], row[5].value))
                            if row[6].value:
                                try:
                                    attrib.AttributeCategoryID = self.__session.query(SqlAlchemy.AttributeCategory).filter(
                                        SqlAlchemy.AttributeCategory.AttributeCategoryName == row[6].value
                                    ).first().AttributeCategoryID
                                except Exception as e:
                                    print e
                                    raise Exception('Error in sheet {}\ncould not find {} in AttributeCategory\n\n'
                                                    .format(sheet_names[3], row[5].value))

                            attrib.ModelInputOrOutput = row[6].value
                            attrib.AttributeDescription = row[7].value
                            self.setup.push_data(attrib)
                        break
    def add_data(self):
        self.setup.add_data()
