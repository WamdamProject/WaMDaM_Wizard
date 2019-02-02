import sqlite3
import numpy as np
import pandas as pd
import getpass
from hs_restclient import HydroShare, HydroShareAuthBasic
import os

import plotly

from plotly.graph_objs import *

import os
import csv
from collections import OrderedDict
import sqlite3
import pandas as pd
import numpy as np
from IPython.display import display, Image, SVG, Math, YouTubeVideo
import urllib

print 'The needed Python libraries have been imported'


username = 'amabdallah'
password = 'MyHydroShareWorld'

auth = HydroShareAuthBasic(username=username, password=password)

hs = HydroShare(auth=auth)
print hs
for resource in hs.resources():
    print 'Connected to HydroShare'
