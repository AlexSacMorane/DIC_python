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
            if l_sample == 66 and c_sample == 50:
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
            u[0] = -(u[0] - dict_user['d_zr'])
            u[1] =  (u[1] - dict_user['d_zr'])
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
            cor = normxcorr2(sample, search_zone[l: l+sample.shape[0], c: c+sample.shape[1]])
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
    return [u_c, u_l]

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
    # init the list 
    L_x = []
    L_y = []
    L_v_x = []
    L_v_y = []

    # iterate on the data from the dic
    for i_data in range(len(dict_user['L_u'])):
        u_i = dict_user['L_u'][i_data]
        lc_sample_i = dict_user['L_lc_sample'][i_data]
        # convert data
        L_x.append(lc_sample_i[1])
        L_y.append(lc_sample_i[0])
        L_v_x.append(u_i[0])
        L_v_y.append(u_i[1])

    # check if you can cheat
    if dict_user['sollicitation'] == 'shearing' or \
       dict_user['sollicitation'] == '2_blocks_x' or \
       dict_user['sollicitation'] == '2_blocks_y' :
        # you can cheat
        L_x_pred = []
        L_y_pred = []
        L_v_x_pred = []
        L_v_y_pred = []
        # predict the solution
        if dict_user['sollicitation'] == 'shearing':
            for i in range(dict_user['domain_size']):
                L_x_pred.append(0)
                L_y_pred.append(i)
                L_v_x_pred.append(dict_user['strain']*dict_user['M_final'].shape[0]*i/(dict_user['domain_size']-1))
                L_v_y_pred.append(0)
        if dict_user['sollicitation'] == '2_blocks_x':
            for i in range(dict_user['domain_size']):
                L_x_pred.append(0)
                L_y_pred.append(i)
                if i < dict_user['domain_size']/2:
                    L_v_x_pred.append(0)
                else : 
                    L_v_x_pred.append(dict_user['strain']*dict_user['M_final'].shape[0])
                L_v_y_pred.append(0)
        if dict_user['sollicitation'] == '2_blocks_y':
            for i in range(dict_user['domain_size']):
                L_x_pred.append(i)
                L_y_pred.append(0)
                L_v_x_pred.append(0)
                if i < dict_user['domain_size']/2:
                    L_v_y_pred.append(0)
                else : 
                    L_v_y_pred.append(-dict_user['strain']*dict_user['M_final'].shape[0])

        # plot
        fig, (ax1, ax2) = plt.subplots(1,2,figsize=(16,9))
        ax1.quiver(L_x, L_y, L_v_x, L_v_y)
        ax1.set_title('dic results', fontsize=25)
        ax2.quiver(L_x_pred, L_y_pred, L_v_x_pred, L_v_y_pred)
        ax2.set_title('dic prediction', fontsize=25)
        fig.tight_layout()
        fig.savefig('images/dic_results.png')
        plt.close(fig)


    else :
        # plot
        fig, (ax1) = plt.subplots(1,1,figsize=(16,9))
        ax1.quiver(L_x, L_y, L_v_x, L_v_y)
        fig.tight_layout()
        fig.savefig('images/dic_results.png')
        plt.close(fig)

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


