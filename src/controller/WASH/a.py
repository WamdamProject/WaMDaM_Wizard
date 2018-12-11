# https://github.com/NREL/gdx-pandas
import pandas as pds
# import XlsxWriter
import gdxpds
from ctypes import c_bool
import logging

import gdxpds.gdx

out_file = 'my_new_gdx_data.gdx'
with gdxpds.gdx.GdxFile() as gdx:
    # Create a new set with one dimension
    gdx.append(gdxpds.gdx.GdxSymbol('my_set',gdxpds.gdx.GamsDataType.Set,dims=['u']))
    data = pds.DataFrame([['u' + str(i)] for i in range(1,11)])
    data['Value'] = True
    gdx[-1].dataframe = data
    # Create a new parameter with one dimension
    gdx.append(gdxpds.gdx.GdxSymbol('my_parameter',gdxpds.gdx.GamsDataType.Parameter,dims=['u']))
    data = pds.DataFrame([['u' + str(i), i*100] for i in range(1,11)],
                         columns=(gdx[-1].dims + gdx[-1].value_col_names))
    gdx[-1].dataframe = data
    gdx.write(out_file)