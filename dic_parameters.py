#-------------------------------------------------------------------------------
# Librairies
#-------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os, shutil, time, pickle, random

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def parameters(dict_user):
    '''
    Read the parmeters defined by the user.
    '''
    # define the zone of study
    dict_user['c_zs_min'] = 10 # column
    dict_user['c_zs_max'] = 90
    dict_user['l_zs_min'] = 10 # line
    dict_user['l_zs_max'] = 90

    # define the sample
    dict_user['d_sample'] = 8

    # define the zone of research
    dict_user['d_zr'] = 8 # increment to sample

    # convert voxel into size
    dict_user['f_voxel_size'] = 1 # m/voxel   
    

