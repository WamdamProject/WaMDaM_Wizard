import pandas as pds
import gdxpds.gdx

from IPython.display import display, Image, SVG, Math, YouTubeVideo




# df=pd.DataFrame(d, index= [1,2,3,], columns=['*', 'value'])

d = {'*': [1, 2], 'value': [30, 40]}
df = pds.DataFrame(data=d)

# assume we have a DataFrame df with last column 'value'
# data_ready_for_GAMS = { 'Qmax': df }
#
# gdx_file = './o_gams.gdx'
# gdx = gdxpds.to_gdx(data_ready_for_GAMS, gdx_file)

display (df)
out_file = 'my_new_gdx_data.gdx'
# with gdxpds.gdx.GdxFile() as gdx:
#     # Create a new set with one dimension
#     # gdx.append(gdxpds.gdx.GdxSymbol('my_set',gdxpds.gdx.GamsDataType.Set,dims=['u']))
#     # data = pds.DataFrame([['u' + str(i)] for i in range(1,11)])
#     # data['Value'] = True
#     # gdx[-1].dataframe = data
#     # Create a new parameter with one dimension
#     gdx.append(gdxpds.gdx.GdxSymbol('my_parameter',gdxpds.gdx.GamsDataType.Parameter,dims=['u']))
#     data = df
#     gdx[-1].dataframe = data
#     gdx.write(out_file)


print 'done'

# with gdxpds.gdx.GdxFile() as gdx:
#     # Create a new set with one dimension
#     gdx.append(gdxpds.gdx.GdxSymbol('my_set',gdxpds.gdx.GamsDataType.Set,dims=['u']))
#     data = pds.DataFrame([['u' + str(i)] for i in range(1,11)])
#     data['Value'] = True
#     gdx[-1].dataframe = data

# wait: do you see the .set and .paramter? the problem we dont have them now in the read data. (set or par)
# I'm not sure how to make the read code, get the type so we can use it in the writing again '
# make sense?
# But maybe try to load all what we have using .set


    # # Create a new parameter with one dimension
    # gdx.append(gdxpds.gdx.GdxSymbol('my_parameter',gdxpds.gdx.GamsDataType.Parameter,dims=['u']))
    # data = pds.DataFrame([['u' + str(i), i*100] for i in range(1,11)],
    #                      columns=(gdx[-1].dims + gdx[-1].value_col_names))
    # gdx[-1].dataframe = data
    # gdx.write(out_file)