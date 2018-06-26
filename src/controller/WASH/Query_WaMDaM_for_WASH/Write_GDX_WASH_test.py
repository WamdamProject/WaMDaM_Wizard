# https://github.com/NREL/gdx-pandas
import pandas as pd
import numpy as np

# import XlsxWriter
import gdxpds
from ctypes import c_bool
from collections import OrderedDict

# from ReadGDX import *
from QueryWAMDAM import Read_provided_file_query_Required

def Prepare_Seasonal_df(total_df_Seasonal):
    # gdx_file = './Test_output2.gdx'
    df_Seasonal = OrderedDict()
    df_Seasonal_dict = []
    # iterate over the attributes to write each of them into a seperate GDX tab
    df_Seasonal_dict = {}
    df_Seasonal_dict['Qmax'] = pd.DataFrame()
    for attribute_df in total_df_Seasonal:
        par_name=attribute_df['AttributeName'][1]
        if par_name=='Qmax': #[1] in ['Qmax', 'Qmin', 'aw', 'instreamReq', 'lss', 'Qsim']:
            # convert the SeasonNumericValue to be float then we use the old code to pass the dataframe and write it
            # attribute_df
            SeasonName = attribute_df['SeasonName'].tolist()
            StartEndNode = attribute_df['StartEndNode'].tolist()
            EndNodeInstance = attribute_df['EndNodeInstance'].tolist()
            dfList = attribute_df['SeasonNumericValue'].tolist()

            x = [float(i) for i in dfList]


            #
            #All we need to do is just to convert the "value" (last column which is SeasonNumericValue) in any frame into a float
    # d=['j1', 'j2','j3','j4','j5','j6','j7','j8','j9','j10','j11','j12']
    d={'*': StartEndNode,'**':EndNodeInstance,'***':SeasonName,'value': x}
    #
    # df = pd.DataFrame(data={'value': d})
    # d = {'*': ['j1', 'j2'], '**': ['a1', 'b2'],'***': ['c1', 'd2'],'value': [30, 40]}
    df = pd.DataFrame(data=d)

    out_file = 'test_may.gdx'
    with gdxpds.gdx.GdxFile() as gdx:
        par_name='test'
        gdx.append(gdxpds.gdx.GdxSymbol(par_name,gdxpds.gdx.GamsDataType.Parameter,dims=['u']))
        data = df
        print data
        gdx[-1].dataframe = data
        gdx.write(out_file)

#
#
total_df_Seasonal, total_df_MultiColumns, total_df_Descriptor, total_df_Numeric,total_df_TimeSeries = Read_provided_file_query_Required()
return_data = Prepare_Seasonal_df(total_df_Seasonal)

# WriteToGdx(return_data)
