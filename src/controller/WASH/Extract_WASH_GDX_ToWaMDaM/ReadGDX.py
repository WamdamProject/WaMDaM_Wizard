# https://github.com/NREL/gdx-pandas
import pandas as pd
# import XlsxWriter
import gdxpds
from ctypes import c_bool
import logging
import gdxpds.gdx

"""
Python dicts of {symbol_name: pandas.DataFrame}, where 
each pandas.DataFrame contains data for a single set, parameter, equation, or 
variable.
"""
# gdx_file = "C:\Users\Adel\Documents\Test_wash\WASH_5yrs_OutputData.gdx"
# gdx_file = "C:\Users\Adel\Documents\Test_wash\Systems-model-in-Wetlands-to-Allocate-water-and-Manage-Plant-Spread\Version1.2-WetlandUnitsAsTanks\GUI_v1.2\BRMBR_Input.gdx"
# read from this one
gdx_file = "C:\Users\Adel\Documents\GitHub\WaMDaM_Wizard_1.04\src\controller\WASH\Extract_WASH_GDX_ToWaMDaM\WASH-Data.gdx"
dataframes = gdxpds.to_dataframes(gdx_file)

# with gdxpds.gdx.GdxFile(lazy_load=False) as f:
#     f.read(gdx_file)
#     for symbol in f:
#         symbol_name = symbol.name
#         df = symbol.dataframe
#         GamsDataType = symbol.data_type.name
#         print("Doing work with {},{}".format(symbol_name,GamsDataType))


# Create a Pandas Excel writer using XlsxWriter as the engine.

#1.
# writer = pd.ExcelWriter('WAHS_input_GDX3_as_is.xlsx', engine='xlsxwriter')
#2.
# writer = pd.ExcelWriter('SWAMPS_Input_GDX.xlsx', engine='xlsxwriter')
#3.
# writer = pd.ExcelWriter('WASH_5yrs_OutputData_5yrs.xlsx', engine='xlsxwriter')

def ReadGdx():

    # except Exception as e:
    #     print e
            # continue
    df_all = {}
    for symbol_name, df in dataframes.items():

        # if symbol_name=='Z' or symbol_name=='Q' or symbol_name=='WSI' or symbol_name=='W': continue
        # if symbol_name=='FlowMarginal' or symbol_name=='lng' or symbol_name=='dReq': continue
        # try:
            # if symbol_name not in 'links':
            #     print("Doing work with {}.".format(symbol_name))
                # print df

                if 'Value' in df.keys():
                    for i, sub_key in enumerate(df['Value']):
                        # if df['Value'][i] == c_bool(True):
                        if len(df['Value']) > i and isinstance(df['Value'][i], c_bool):
                            df['Value'][i] = True

                # sotre all the dfs from here so we can pass them to another function
                # keep the symbol_name with each df
                df_all[symbol_name] = df


                 # Convert the dataframe to an XlsxWriter Excel object.
                # df.to_excel(writer, sheet_name=symbol_name)
                #Save each data from into a sheet in one excel file



                # Close the Pandas Excel writer and output the Excel file.
    # writer.save()

    return df_all

# to view the frames in Excel (for fun)
def WriteToWaMDaM(df_all):

    # read the the j paramter and pass it to the function write_nodes that exist in this file Write_WaMDaM_Workbook
    # use the paramter name "j" for ObjectType value
    # use the paramter values for the NodeInstanceName
    filename="WAHS_input_GDX_1_year_as_is.xlsx"

    from Write_GDX_TO_WaMDaM_Workbook import SaveExcel
    SaveExcel(df_all, filename)


# df.to_excel(writer, sheet_name=symbol_name)

df_all = ReadGdx()
WriteToWaMDaM(df_all)