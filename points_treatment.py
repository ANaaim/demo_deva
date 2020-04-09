# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:18:11 2019

@author: AdminXPS
"""
import numpy as np
from scipy import signal, interpolate


def points_treatment(acq, fc_marker,unit_point='mm'):
    points_temp = acq['data']['points'][0:3, :, :]
    points = np.zeros_like(points_temp)

    # Respect ISB convention
    if unit_point =='mm':
        unit_conv = 1000
    elif unit_point == 'm':
        unit_conv = 1
    else:
        print('unit_point in point_treatment is not supported')
    
    points[0] = points_temp[0]/unit_conv
    points[1] = points_temp[2]/unit_conv
    points[2] = -points_temp[1]/unit_conv
    # FIXME : Modify point treatment whe
    # points = np.array(points)
    nb_frame = points.shape[2]
    frq_acq = acq['parameters']['POINT']['RATE']['value'][0]

    order_marker = 4.0

    x = np.arange(0, nb_frame)
    f = interpolate.interp1d(x, points, axis=2)
    points_interp = f(tuple(x))
    # Filtering
    b, a = signal.butter(order_marker, fc_marker/(0.5*frq_acq))
    points_treated = signal.filtfilt(b, a, points_interp, axis=2)

    return points_treated
