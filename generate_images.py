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

def create_folder(name):
    '''
    Create a new folder.
    '''
    if Path(name).exists():
        shutil.rmtree(name)
    os.mkdir(name)

#-------------------------------------------------------------------------------

def print_image(M, title, namefile):
    '''
    Generate an image of the microstructure.
    '''
    # plot
    fig, (ax1) = plt.subplots(1,1,figsize=(16,9))
    im = ax1.imshow(M)
    ax1.set_title(title,fontsize = 30)
    fig.tight_layout()
    fig.savefig(namefile)
    plt.close(fig)

#-------------------------------------------------------------------------------

def pure_shearing(dict_user):
    '''
    Apply a pure shearing to an image.
    '''
    # apply random spekkle pattern
    for i in range(dict_user['domain_size']):
        # compute the strain applied in the line
        strain_i = dict_user['strain']*dict_user['M_final'].shape[0]*i/(dict_user['domain_size']-1)
        for j in range(dict_user['domain_size']):
            # interpolate the pixel
            pass

    # plot 
    print_image(dict_user['M_final'], r'Final map', 'images/M_1.png')

#-------------------------------------------------------------------------------
# Parameter
#-------------------------------------------------------------------------------

# domain 
domain_size = 100 # same in 2 directions

# available: shearing
sollicitation = 'shearing'

# depending on the sollicitation, the strain applied
strain = 0.05 # -

#------------------------------------------------------------------------------
# create dict
#------------------------------------------------------------------------------

dict_user = {
    'domain_size' : domain_size,
    'sollicitation' : sollicitation,
    'strain' : strain
}

#-------------------------------------------------------------------------------
# Plan simulation
#-------------------------------------------------------------------------------

create_folder('images')

#-------------------------------------------------------------------------------
# Generation of the microstructure
#-------------------------------------------------------------------------------

# initialization
dict_user['M_initial'] = np.array(np.zeros((dict_user['domain_size'], dict_user['domain_size'])))

# apply random spekkle pattern
for i in range(dict_user['domain_size']):
    for j in range(dict_user['domain_size']):
        dict_user['M_initial'][i, j] = random.random()

# plot
print_image(dict_user['M_initial'], r'Initial map', 'images/M_0.png')

#-------------------------------------------------------------------------------
# Apply strain
#-------------------------------------------------------------------------------

# create a copy
dict_user['M_final'] = dict_user['M_initial'].copy()

# selection of the deformation applied
if dict_user['sollicitation'] == 'shearing':
    pure_shearing(dict_user)

#-------------------------------------------------------------------------------
# save dict
#-------------------------------------------------------------------------------

with open('images/dict_user', 'wb') as handle:
    pickle.dump(dict_user, handle, protocol=pickle.HIGHEST_PROTOCOL)
