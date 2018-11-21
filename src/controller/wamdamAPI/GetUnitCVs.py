from ..ConnectDB_ParseExcel import DB_Setup


import pandas as pd

class GetUnits(object):
    def __init__(self):
        self.setup = DB_Setup()

        self.session = self.setup.get_session()
    def GetUnits_dims(self):
        UnitsDims_sql_command = """SELECT Name as UnitName, Category as Dimension ,UnitAbbreviation
                                FROM CV_Units  
                                WHERE Dimension !='' and  Dimension is not null
                                ORDER by Dimension ASC
                                    """
        UnitsDims_Result_df =  pd.DataFrame(list( self.session.execute(UnitsDims_sql_command)))
        return UnitsDims_Result_df

