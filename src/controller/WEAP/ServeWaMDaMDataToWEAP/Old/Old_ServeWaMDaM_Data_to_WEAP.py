
import win32com.client
from controller.ConnectDB_ParseExcel import DB_Setup
from controller.ConnectDB_ParseExcel import SqlAlchemy as sq

from sqlalchemy.orm import aliased
# 1. Connect to WEAP

# Function to create the connection with WEAP
class WEAP_export(object):

    WEAP = None

    def __init__(self):
        self.ConnectWEAP()
        self.setup = DB_Setup()
        self.session = self.setup.get_session()
        self.excel_pointer = None

    def ConnectWEAP(self):

        self.WEAP=win32com.client.Dispatch("WEAP.WEAPApplication")

        # make this dynamic active area
        self.WEAP.ActiveArea = "BearRiverFeb2017_V10.9"

        ActiveArea=self.WEAP.ActiveArea.Name
        Scenario=self.WEAP.ActiveScenario.Name

        WEAPAreasDirectory= self.WEAP.AreasDirectory

        print ActiveArea
        print Scenario
        print WEAPAreasDirectory
        SourceName=self.WEAP.ActiveArea.Name

    # 2. Extract the WEAP Network



    def QueryWaMDaMDataForWEAP(self):
        # call the function wich will run the query and write its output to excel

        # Time Series
        from controller.WEAP.ServeWaMDaMDataToWEAP.QueryTimeSeries import TimeSeries_query, Timeseries_csv_file
        df_TimeSeries = TimeSeries_query(self.session)
        csv_file_name_timeseries = Timeseries_csv_file(df_TimeSeries)


        # Multi Columns
        from controller.WEAP.ServeWaMDaMDataToWEAP.QueryMultiAttributes import MultiAttributes_query, MultiAttributes_csv_file
        df_MultiColumns = MultiAttributes_query(self.session)
        csv_file_path_or_value_multi = MultiAttributes_csv_file(df_MultiColumns)


        # Seasonal
        from controller.WEAP.ServeWaMDaMDataToWEAP.QuerySeasonal import Seasonal_query, Seasonal_csv_file
        df_Seasonal = Seasonal_query(self.session)
        csv_file_path_or_value_seasonal = Seasonal_csv_file(df_Seasonal)

        # Metadata for all the files together (pass all these to the function
        from controller.WEAP.ServeWaMDaMDataToWEAP.ExportWEAP_Input_metadata_file import WriteMetadataFile
        WriteMetadataFile(df_TimeSeries, df_MultiColumns, df_Seasonal,
                          csv_file_name_timeseries, csv_file_path_or_value_seasonal,
                          csv_file_path_or_value_multi)
        WriteMetadataFile(self)



if __name__ == '__main__':
    weap_export = WEAP_export()
    weap_export.QueryWaMDaMDataForWEAP()

# so here I want to run Extract_Network function and get back its resutls


