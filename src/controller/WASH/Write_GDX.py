# https://github.com/NREL/gdx-pandas
import pandas as pd

# import XlsxWriter
import gdxpds
from ctypes import c_bool

from ReadGDX import *

def WriteToGdx(df_all):
    # Option 1. Simple
    # assume we have a DataFrame df with last column 'value'
    gdx_file = 'C:\RC\Final_Wizard_April_2018\controller\WASH\Test5.gdx'
    with gdxpds.gdx.GdxFile() as gdx:
        for df in df_all:
            if df == 'InitSTOR':

            #     if df=='lng':
        #         data_ready_for_GAMS = { df: df_all[df] }
        #         gdx = gdxpds.to_gdx(data_ready_for_GAMS, gdx_file)


        #
        # # Option 2. More control
        # out_file = 'test_output.gdx'
        #     with gdxpds.gdx.GdxFile() as gdx:

                # Create a new set with one dimension
                    # sets
                if len(df_all[df]['Value']) < 1 or isinstance(df_all[df]['Value'][0], bool):
                    gdx.append(gdxpds.gdx.GdxSymbol(df,gdxpds.gdx.GamsDataType.Set,dims=['u']))
                else:
                    # paramters
                    gdx.append(gdxpds.gdx.GdxSymbol(df, gdxpds.gdx.GamsDataType.Parameter, dims=['u']))
                # data = pd.DataFrame([['u' + str(i)] for i in range(1,11)])
                # data['Value'] = True
                gdx[-1].dataframe = df_all[df]

        #
        #     # Create a new parameter with one dimension
        #     gdx.append(gdxpds.gdx.GdxSymbol('my_parameter',gdxpds.gdx.GamsDataType.Parameter,dims=['u']))
        #     data = pd.DataFrame([['u' + str(i), i*100] for i in range(1,11)],
        #                          columns=(gdx[-1].dims + gdx[-1].value_col_names))
        #     gdx[-1].dataframe = data
                gdx.write(gdx_file)

df_all = ReadGdx()
WriteToGdx(df_all)