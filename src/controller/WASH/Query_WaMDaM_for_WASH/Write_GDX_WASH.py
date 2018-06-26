# https://github.com/NREL/gdx-pandas
import pandas as pd

# import XlsxWriter
import gdxpds
from ctypes import c_bool
from collections import OrderedDict

# from ReadGDX import *
from QueryWAMDAM import Read_provided_file_query_Required

def Prepare_Seasonal_df(total_df_Seasonal):
    df_Seasonal = OrderedDict()
    # df_Seasonal_dict = []
    # iterate over the attributes to write each of them into a seperate GDX tab
    df_Seasonal_dict = {}
    # df_Seasonal_dict['Qmax'] = pd.DataFrame()
    for attribute_df in total_df_Seasonal:
        # if attribute_df['AttributeName'][1]=='aw': #[1] in ['Qmax', 'Qmin', 'aw', 'instreamReq', 'lss', 'Qsim']:
            # check if the AttributeName is the same, if so append the data frame
            key = attribute_df['AttributeName'][1]
            if not key in df_Seasonal_dict.keys():
                df_Seasonal_dict[attribute_df['AttributeName'][1]] = []
            # here it should be appended with ~10 frames. then we pass it as one big frame
            df_Seasonal = pd.DataFrame()
            # print df_Seasonal
    #         for idx, attribute_df_StartEndNode in enumerate(attribute_df['StartEndNode']):
            if attribute_df['StartEndNode'][1]!='':  # if the start node exist, then write start and end nodes
                df_Seasonal['*'] = pd.Series(data=attribute_df['StartEndNode'])
                df_Seasonal['**'] = pd.Series(data=attribute_df['EndNodeInstance'])
            if attribute_df['StartEndNode'][1]=='':
                    df_Seasonal['**'] = pd.Series(data=attribute_df['NodeORLinkInstanceName'])
            df_Seasonal['***'] = pd.Series(data=attribute_df['SeasonName'])
            df_Seasonal['***'] = pd.Series(data=attribute_df['SeasonName'])
            Value_float = [float(i) for i in attribute_df['SeasonNumericValue']]
            df_Seasonal['value'] = pd.Series(data=Value_float)
            df_Seasonal_dict[key].append(df_Seasonal)

    # WriteToGdx(df_Seasonal_dict)
    df_results = {}
    for key in df_Seasonal_dict:
        if len(df_Seasonal_dict[key]) > 1:
            frame = pd.concat(df_Seasonal_dict[key])
            df_results[key] = frame
        else:
            df_results[key] = df_Seasonal_dict[key][0]
    return df_results



def Prepare_MultiAtt_df(total_df_MultiColumns):
    # df_MultiAttr = OrderedDict()
    # df_MultiAttr_dict = []
    # iterate over the attributes to write each of them into a seperate GDX tab
    df_MultiAttr_dict = {}
    # df_MultiAttr_dict['Qmax'] = pd.DataFrame()
    for attribute_df in total_df_MultiColumns:
        df_MultiAttr = pd.DataFrame()
        many_df_MultiAttr= pd.DataFrame()
        # if attribute_df['MultiAttributeName'][1]=='rsi_par': #and attribute_df['NodeORLinkInstanceName'][1]=='j34j33': #[1] in ['Qmax', 'Qmin', 'aw', 'instreamReq', 'lss', 'Qsim']:
            # check if the AttributeName is the same, if so append the data frame
        t_datas = []
        other_att = []
        other_vals = []
        other_val_orders = []
        for i, atts in enumerate(attribute_df['AttributeName']):
            if atts == 't':
                t_datas.append(attribute_df['DataValue'][i])
            else:
                other_att.append(atts)  # to get rsi_par, etc
                other_vals.append(attribute_df['DataValue'][i])
                other_val_orders.append(attribute_df['ValueOrder'][i])
        # if the 't' exist, then prepare the data frame that has it
        if len(t_datas) > 0:
            starts =[]
            ends = []
            total_count_row = len(other_vals)
            for i in range(total_count_row):
                starts.append(attribute_df['StartEndNode'][i])
                ends.append(attribute_df['EndNodeInstance'][i])
            df_MultiAttr['StartEndNode'] = pd.Series(data=starts)
            df_MultiAttr['EndNodeInstance']=pd.Series(data=ends)

            repeat_count = len(other_vals) / len(t_datas)
            final_t_datas = []
            for i, order in enumerate(other_val_orders):
                final_t_datas.append(t_datas[order-1])


            df_MultiAttr['t'] = pd.Series(data=final_t_datas)
            df_MultiAttr['AttributeName']  = pd.Series(data=other_att)# value: rsi_par, etc
            df_MultiAttr['DataValue'] = pd.Series(data=other_vals)
            # df_MultiAttr = df_MultiAttr.sort_values(['t', 'MultiAttributeName'], ascending=[True, False])



            # prepare the data frames above as needed (use df_MultiAttr as input)
            df_MultiColumns_gdx = pd.DataFrame()
            # print df_Seasonal
            #         for idx, attribute_df_StartEndNode in enumerate(attribute_df['StartEndNode']):
            if df_MultiAttr['StartEndNode'][1] != '':  # if the start node exist, then write start and end nodes

                df_MultiColumns_gdx['*'] =pd.Series(data=df_MultiAttr['StartEndNode'])
                df_MultiColumns_gdx['**'] = pd.Series(data=df_MultiAttr['EndNodeInstance'])

            if attribute_df['StartEndNode'][1] == '':
                df_MultiColumns_gdx['*']=pd.Series(data=df_MultiAttr['NodeORLinkInstanceName'])
            df_MultiColumns_gdx['***'] = pd.Series(data=df_MultiAttr['t'])
            df_MultiColumns_gdx['****'] = pd.Series(data=df_MultiAttr['AttributeName'])

            Value_float = [float(i) for i in df_MultiAttr['DataValue']]
            df_MultiColumns_gdx['value'] = pd.Series(data=Value_float)

            # merge into one big frame
            key = attribute_df['MultiAttributeName'][1]
            # appemd frames if they share the same MultiAttributeName
            # df_MultiAttr_dict[key].append(df_MultiColumns_gdx)
            if not key in df_MultiAttr_dict.keys():
                df_MultiAttr_dict[attribute_df['MultiAttributeName'][1]] = []
            df_MultiAttr_dict[key].append(df_MultiColumns_gdx)


        else:
            ############################## t value don't exist  ###########################
            pass

    df_results = {}
    for key in df_MultiAttr_dict:
        if len(df_MultiAttr_dict[key]) > 1:
            frame = pd.concat(df_MultiAttr_dict[key])
            df_results[key] = frame
        else:
            df_results[key] = df_MultiAttr_dict[key][0]
    return df_results

    # df_results: do we need to change the name if this one? one for seasonal and anoither for multi-columns?
# ok

# df_results_seasonal
# df_results_multiCols

def WriteToGdx(df_results):
    gdx_file = 'Output_both.gdx'

    # df_all=df_results
# def WriteToGdx(df_all):
    # assume we have a DataFrame df with last column 'value'
    # gdx_file = './test1ds.gdx'
    # for df in df_all:
    with gdxpds.gdx.GdxFile() as gdx:
        for df_all in df_results:
            for df in df_all:
        #         data_ready_for_GAMS = { df: df_all[df] }
        #         gdx = gdxpds.to_gdx(data_ready_for_GAMS, gdx_file)
        #         print df
        #         df='Qmax2'
                my_parameter=df
                print my_parameter
                x='{}'.format(my_parameter)
                gdx.append(gdxpds.gdx.GdxSymbol(x, gdxpds.gdx.GamsDataType.Parameter, dims=['u']))
                # print df_all[df]['DataValue']
                dfxx = pd.DataFrame(data=df_all[df])

                gdx[-1].dataframe = dfxx
                gdx.write(gdx_file)

total_df_Seasonal, total_df_MultiColumns, total_df_Descriptor, total_df_Numeric,total_df_TimeSeries = Read_provided_file_query_Required()



return_data2 = Prepare_MultiAtt_df(total_df_MultiColumns)


return_data = Prepare_Seasonal_df(total_df_Seasonal)

passlist = [return_data, return_data2]
WriteToGdx(passlist)