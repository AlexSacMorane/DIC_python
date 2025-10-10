#-------------------------------------------------------------------------------
# Librairies
#-------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os, shutil, time, pickle, random, math

# own
from dic_parameters import parameters

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def dic(dict_user):
    '''
    Apply the DIC algorithm.
    '''
    # initialization 
    l_sample = dict_user['l_zs_min']
    L_u = []
    L_lc_sample = []   
    # iterate on lines for sample
    while l_sample < dict_user['l_zs_max']:
        # user
        print(l_sample, '/', dict_user['l_zs_max'])

        # initialization of the sample
        c_sample = dict_user['c_zs_min']
        # iterate on column for sample
        while c_sample < dict_user['c_zs_max']:
            # define sample
            sample = dict_user['M_final'][-1-l_sample-dict_user['d_sample']:-1-l_sample, c_sample:c_sample+dict_user['d_sample']]
            # define search zone
            search_zone = dict_user['M_initial'][-1-l_sample-dict_user['d_sample']-dict_user['d_zr']:-1-l_sample+dict_user['d_zr'], c_sample-dict_user['d_zr']:c_sample+dict_user['d_sample']+dict_user['d_zr']]            
            # plot sample and search zone
            if l_sample == dict_user['l_zs_min'] and c_sample == dict_user['c_zs_min']:
                fig, (ax1, ax2) = plt.subplots(1,2,figsize=(16,9))
                im = ax1.imshow(sample, vmin=np.min(dict_user['M_initial']), vmax=np.max(dict_user['M_initial']))
                ax1.set_title('sample',fontsize = 30)
                im = ax2.imshow(search_zone, vmin=np.min(dict_user['M_initial']), vmax=np.max(dict_user['M_initial']))
                ax2.set_title('search_zone',fontsize = 30)
                fig.tight_layout()
                fig.savefig('images/sample_searchZone.png')
                plt.close(fig)
                # look sample in the search zone
                u = look_sample_in_search_zone(sample, search_zone, True)
            else:
                u = look_sample_in_search_zone(sample, search_zone, False)
            # adapt u
            u[0] = u[0] - dict_user['d_zr']
            u[1] = u[1] - dict_user['d_zr']
            # save 
            L_u.append(u)
            L_lc_sample.append([l_sample, c_sample])
            # next column
            c_sample = c_sample + dict_user['d_sample']
        # next line
        l_sample = l_sample + dict_user['d_sample']
    # save
    dict_user['L_u'] = L_u
    dict_user['L_lc_sample'] = L_lc_sample

#-------------------------------------------------------------------------------

def look_sample_in_search_zone(sample, search_zone, debug):
    '''
    Search sample in the search zone.
    '''
    # initialization
    u_l = 0
    u_c = 0
    cor_max = 0
    if debug:
         M_cor = np.zeros((search_zone.shape[0]-sample.shape[0], search_zone.shape[1]-sample.shape[1]))
    # iterate on lines and column in search_zone
    for l in range(search_zone.shape[0]-sample.shape[0]):
        for c in range(search_zone.shape[1]-sample.shape[1]):
            cor = normxcorr2(sample, search_zone[-1-l-sample.shape[0]: -1-l, c: c+sample.shape[1]])
            if debug:
                M_cor[l, c] = cor
            # look for the maximum value
            if cor > cor_max:
                cor_max = cor
                # change
                u_l = l
                u_c = c
    # print
    if debug:
        fig, (ax1) = plt.subplots(1,1,figsize=(16,9))
        im = ax1.imshow(M_cor)
        ax1.set_title('Map of correlation',fontsize = 30)
        fig.tight_layout()
        fig.savefig('images/correlation.png')
        plt.close(fig)
    return [u_l, u_c]

#-------------------------------------------------------------------------------

def normxcorr2(M_sample, M_sz):
    '''
    Normalized 2-D cross-correlation.
    '''
    # initialization of sums
    S_xy = 0.
    S_x2 = 0.
    S_y2 = 0.
    # iterate on lines and columns
    for l in range(M_sample.shape[0]):
        for c in range(M_sample.shape[1]):
            S_xy = S_xy + (M_sample[l,c] - np.mean(M_sample))*(M_sz[l,c] - np.mean(M_sz))
            S_x2 = S_x2 + (M_sample[l,c] - np.mean(M_sample))**2
            S_y2 = S_y2 + (M_sz[l,c] - np.mean(M_sz))**2
    # compute correlation
    cor = S_xy/(math.sqrt(S_x2)*math.sqrt(S_y2))
    return cor

#-------------------------------------------------------------------------------

def pp(dict_user):
    '''
    Post-process the dic output
    '''
    pass

#------------------------------------------------------------------------------
# load dict
#------------------------------------------------------------------------------

with open('images/dict_user', 'rb') as handle:
    dict_user = pickle.load(handle)

#------------------------------------------------------------------------------
# load parameters
#------------------------------------------------------------------------------

parameters(dict_user)

#------------------------------------------------------------------------------
# apply dic
#------------------------------------------------------------------------------

dic(dict_user)

#------------------------------------------------------------------------------
# pp and plot
#------------------------------------------------------------------------------

pp(dict_user)

