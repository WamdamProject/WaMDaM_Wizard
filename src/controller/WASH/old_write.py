#                 # SeasonName
#                 # SeasonNumericValue
#                 #
#                 # df_Seasonal['start']=attribute_df['StartEndNode']
#                 # df_Seasonal['AttributeName']=attribute_df['AttributeName']
#                 # df_Seasonal['end']=attribute_df['EndNodeInstance']
#                 # df_Seasonal['Season']=attribute_df['SeasonName']
#                 # df_Seasonal['Value']=attribute_df['SeasonNumericValue']
#                 # df = pd.DataFrame(data=df_Seasonal)
#
#                     # can you show the values inside the appended dic?
#
#                     # this result here should look like multiple df(s) appended on top of each others vertically
#                     # we select a few columns from the original df(s)
#                     # lets first make this show up correctly. make sense?
#                     # df_Seasonal_dict
#
#
#                 # with gdxpds.gdx.GdxFile() as gdx:
#                 #     # for df in df_Seasonal_list:
#                 #     gdx.append(gdxpds.gdx.GdxSymbol(df, gdxpds.gdx.GamsDataType.Parameter, dims=['u']))
#                 #     gdx[-1].dataframe = df['AttributeName']
#                 # else:
#                 #     df_Seasonal['Instance']=attribute_df['NodeORLinkInstanceName'][idx]
#                 #     df_Seasonal['Season']=attribute_df['SeasonName'][idx]
#                 #     df_Seasonal['Value']=attribute_df['SeasonNumericValue'][idx]
#                 #     df_Seasonal_dict[attribute_df['AttributeName'][1]].append(df_Seasonal)
#
#                     # prepare the df_Seasonal_list to be silmilair
#     #
#     # with gdxpds.gdx.GdxFile() as gdx:
#     #     for df in df_Seasonal_dict:
#     #         gdx.append(gdxpds.gdx.GdxSymbol(df, gdxpds.gdx.GamsDataType.Parameter, dims=['u']))
#     #     gdx[-1].dataframe = df_Seasonal_dict[df].T
#     # gdx.write(gdx_file)
#     #
#     # print 'done'
#     #
#     #             with gdxpds.gdx.GdxFile() as gdx:
#     #                 for df in df_all:
#     #                     if df == 'Qmax':
#     #                         #     if df=='lng':
#     #                         #         data_ready_for_GAMS = { df: df_all[df] }
#     #                         #         gdx = gdxpds.to_gdx(data_ready_for_GAMS, gdx_file)
#     #
#     #                         #
#     #                         # # Option 2. More control
#     #                         # out_file = 'test_output.gdx'
#     #                         #     with gdxpds.gdx.GdxFile() as gdx:
#     #
#     #                         # Create a new set with one dimension
#     #                         # sets
#     #                         if len(df_all[df]['Value']) < 1 or isinstance(df_all[df]['Value'][0], bool):
#     #                             gdx.append(gdxpds.gdx.GdxSymbol(df, gdxpds.gdx.GamsDataType.Set, dims=['u']))
#     #                         else:
#     #                             # paramters
#     #                             gdx.append(gdxpds.gdx.GdxSymbol(df, gdxpds.gdx.GamsDataType.Parameter, dims=['u']))
#     #                         # data = pd.DataFrame([['u' + str(i)] for i in range(1,11)])
#     #                         # data['Value'] = True
#     #                         gdx[-1].dataframe = df_all[df]
#     #                     gdx.write(gdx_file)
#
#                         #
#             #     # Create a new parameter with one dimension
#             #     gdx.append(gdxpds.gdx.GdxSymbol('my_parameter',gdxpds.gdx.GamsDataType.Parameter,dims=['u']))
#             #     data = pd.DataFrame([['u' + str(i), i*100] for i in range(1,11)],
#             #                          columns=(gdx[-1].dims + gdx[-1].value_col_names))
#             #     gdx[-1].dataframe = data


            # break
        #
    # # Option 2. More control
    # out_file = 'test_output.gdx'
    #     with gdxpds.gdx.GdxFile() as gdx:

            # Create a new set with one dimension
                # sets
                # if len(df_all[df]['value']) < 1 or isinstance(df_all[df]['value'][0], bool):
                #     gdx.append(gdxpds.gdx.GdxSymbol(df,gdxpds.gdx.GamsDataType.Set,dims=['u']))
                # else:
                #     # paramters
                #     gdx.append(gdxpds.gdx.GdxSymbol(df, gdxpds.gdx.GamsDataType.Parameter, dims=['u']))
                # # data = pd.DataFrame([['u' + str(i)] for i in range(1,11)])
                # # data['Value'] = True
                #
                # gdx[-1].dataframe = df_all[df]

        #
        #     # Create a new parameter with one dimension
        #     gdx.append(gdxpds.gdx.GdxSymbol('my_parameter',gdxpds.gdx.GamsDataType.Parameter,dims=['u']))
        #     data = pd.DataFrame([['u' + str(i), i*100] for i in range(1,11)],
        #                          columns=(gdx[-1].dims + gdx[-1].value_col_names))
        #     gdx[-1].dataframe = data
        #     gdx.write(gdx_file)
# def run_func():