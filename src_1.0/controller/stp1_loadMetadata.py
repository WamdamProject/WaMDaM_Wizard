# stp1_loadMetadata.py

'''
    The load_step_1.py file is used to load MetaData excel files
    to the sqlite database using sqlalchemy.
    It Inherits properties from the Parse_Excel_File and DB_Setup
    classes.
    It is primarily made up of:
    - LoadMetaData():   This is the main and only class in this file.
                        it inherits methods for two other classes so as
                        to achieve its task. This class is made up of a
                        constructor used to initialize the other classes,
                        setup the session which is a private variable and
                        also initialize the work_sheet variable which holds
                        all data from sheets in the excel files.
    Important methods and Variables of the class:
    - load_data():  This is a method which does all the processing of each MetaData.
                    it functions by iterating through the work_sheet dictionary, and
                    for each sheet parse the data appropriately so as to store in the
                    required table and fields.
    - work_sheet:   This a dictionary having metadata sheet as keys and the sheet
                    data as values. its data is gotten from the
                    parse_object_control_value() method found in Parse_Excel_File class.
    - __session:    Session variables (private) used to access the database.
'''

# We Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from .ConnectDB_ParseExcel import *

# We Import the this class so as to change some none ascii characters found in the excel file to ascii
import unicodedata

# We import required variables (this are the metadata sheet names and their start values in the excel file)
from .ReadWorkbook_SheetsNames import metadata_sheets_ordered



# ****************************************************************************************************************** #
#                                                                                                                    #
#                                         Script Begins here                                                         #
#                                                                                                                    #
# ****************************************************************************************************************** #



class LoadMetaData(Parse_Excel_File):
    """
        Class used to load MetaData to tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """
    def __init__(self, filename):
        """
        This is the LoadMetaData Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(LoadMetaData, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value(metadata_sheets_ordered[:])

    def load_data(self):
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
        :return: None
        """
        static_rownum = 10
        for sheet_name, sheet_rows in self.work_sheet.items():
            temp = sheet_rows[:]
            for row_id, row in enumerate(temp):
                temp_row = [cell.value for cell in row]

                if sheet_name == metadata_sheets_ordered[0]:
                    # Loading Organizations data into the database
                    if 'Organizations_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        temp_org = cur_table[:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum
                            temp_row = [cell.value for cell in row]

                            if all('' == cell.value for cell in row):
                                break
                            result = []
                            for cell in row:
                                try:
                                    cell = cell.value.replace(u"\u2018", "'").replace(u"\u2019", "'")
                                except:
                                    pass
                                result.append(cell)
                            row = result
                            org = SqlAlchemy.Organizations()
                            if row[0] == "":
                                raise Exception('Error in Organizations_table\'s {} row of sheet "{}"\nField named "OrganizationName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[0]))

                            existname = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                    SqlAlchemy.Organizations.OrganizationName == row[0]
                                ).first()
                            if existname == None:
                                org.OrganizationName = row[0]
                                org.OrganizationType = row[1]
                                org.OrganizationWebpage = row[2]
                                org.Description = row[3]
                                self.setup.push_data(org)

                    # Loading People data into the database
                    if 'People_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum + 11
                            if all('' == cell.value for cell in row):
                                break
                            result = []

                            '''Check a wrong letter and replace letter "'". And if value of the cell is not string, exception is occured.'''
                            for cell in row:
                                try:
                                    cell = cell.value.replace(u"\u2018", "'").replace(u"\u2019", "'")
                                except:
                                    pass
                                    # raise Exception('Error in "People_table" {} row of sheet "{}"\nThere is a non-string value on this row. \nPlease fix the value to string.'
                                    #             .format(row_id + 1, metadata_sheets_ordered[0]))
                                result.append(cell)
                            row = result
                            pple = SqlAlchemy.People()
                            if row[0] == "":
                                raise Exception('Error in "People_table" {} row of sheet "{}"\nField named "PersonName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[0]))

                            if row[6] == "":
                                raise Exception('Error in "People_table" {} row of sheet "{}"\nField named "OrganizationName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[0]))

                            name = unicodedata.normalize("NFKD", row[0])
                            existname = self.__session.query(SqlAlchemy.People).filter(
                                    SqlAlchemy.People.PersonName == name
                                ).first()
                            if existname == None:
                                pple.PersonName = name
                                pple.Address = row[1]
                                pple.Email = row[2]
                                pple.Phone = str(row[3])
                                pple.PersonWebpage = row[4]
                                pple.Position = row[5]
                                try:
                                    pple.OrganizationID = self.__session.query(SqlAlchemy.Organizations).filter(
                                        SqlAlchemy.Organizations.OrganizationName == row[6]
                                    ).first().OrganizationID
                                except Exception as e:
                                    raise Exception("Error with sheet {} on row {}\ncould not find {} in Organization."
                                                    .format(metadata_sheets_ordered[1], row_id+1, row[6]))
                                self.setup.push_data(pple)
                        break

                elif sheet_name == metadata_sheets_ordered[1]:

                    # Loading Sources data into the Database
                    if 'Sources_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        temp_org = cur_table[:]
                        for row_id, row in enumerate(cur_table):
                            temp_row = [cell.value for cell in row]
                            row_id = row_id + static_rownum -2
                            if all('' == cell.value for cell in row):
                                break
                            result = []
                            for cell in row:
                                try:
                                    cell = cell.value.replace(u"\u2018", "'").replace(u"\u2019", "'")
                                except:
                                    pass
                                result.append(cell)
                            row = result
                            source = SqlAlchemy.Sources()
                            if row[0] == "":
                                raise Exception('Error in Sources_table\'s {} row of sheet "{}"\nField named "SourceName" is empty.\n\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[1]))

                            if row[3] == "":
                                raise Exception('Error in Sources_table\'s {} row of sheet "{}"\nField named "PersonName" is empty.\n\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[1]))
                            name = row[0].replace(u"\u2018", "'").replace(u"\u2019", "'")
                            existname = self.__session.query(SqlAlchemy.Sources).filter(
                                    SqlAlchemy.Sources.SourceName == name
                                ).first()
                            if existname == None:
                                source.SourceName = row[0].replace(u"\u2018", "'").replace(u"\u2019", "'")
                                source.SourceWebpage = row[1]
                                source.SourceCitation = row[2]
                                try:
                                    row[3] = unicodedata.normalize('NFKD', row[3])
                                    source.PersonID = self.__session.query(SqlAlchemy.People).filter(
                                        SqlAlchemy.People.PersonName == row[3]
                                    ).first().PersonID
                                except Exception as e:
                                    raise Exception("Error with sheet {} on row {}\ncould not find {} in People"
                                                    .format(metadata_sheets_ordered[2], row_id+8, row[3]))
                                source.Description = row[4]
                                self.setup.push_data(source)

                    # Loading Method data into the Database
                    if 'Methods_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum + 8
                            if all('' == cell.value or ' ' == cell.value for cell in row):
                                break
                            result = []
                            for cell in row:
                                try:
                                    cell = cell.value.replace(u"\u2018", "'").replace(u"\u2019", "'")
                                except:
                                    pass
                                result.append(cell)
                            row = result
                            method = SqlAlchemy.Methods()
                            if row[0] == "":
                                raise Exception('Error in {} row of "Methods_table" of sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[1]))
                            if row[3] == "":
                                raise Exception('Error in {} row of "Methods_table" of sheet "{}"\nField named "MethodTypeCV" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[1]))
                            if row[4] == "":
                                raise Exception('Error in {} row of "Methods_table" of sheet "{}"\nField named "PersonName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                                .format(row_id, metadata_sheets_ordered[1]))
                            name = row[0].replace(u"\u2018", "'").replace(u"\u2019", "'")
                            existname = self.__session.query(SqlAlchemy.Methods).filter(
                                    SqlAlchemy.Methods.MethodName == name
                                ).first()
                            if existname == None:
                                method.MethodName = row[0].replace(u"\u2018", "'").replace(u"\u2019", "'")
                                method.MethodWebpage = row[1]
                                method.MethodCitation = row[2]
                                try:
                                    method.MethodTypeCV = self.__session.query(SqlAlchemy.CV_MethodType).filter(
                                        SqlAlchemy.CV_MethodType.Name == row[3]
                                    ).first().Name
                                except Exception as e:
                                    raise Exception('Error with sheet "{}"\ncould not find "{}" in MethodType'
                                                    .format(metadata_sheets_ordered[1], row[3]))
                                try:
                                    method.PersonID = self.__session.query(SqlAlchemy.People).filter(
                                        SqlAlchemy.People.PersonName == unicodedata.normalize("NFKD", row[4])
                                    ).first().PersonID
                                except Exception as e:
                                    raise Exception('Error with sheet "{}"\ncould not fine "{}" in People'
                                                    .format(metadata_sheets_ordered[1], row[4]))
                                method.Description = row[5]
                                self.setup.push_data(method)
                        break

    def add_data(self):
        self.setup.add_data()
