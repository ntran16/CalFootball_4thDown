import pandas as pd
import numpy as np
import cal_football as cf

def exp_net_punt_dist_model(punts):
    def curve_fit(x, y, smoothness=.5):
        from statsmodels.nonparametric.smoothers_lowess import lowess
        results = lowess(y, x, is_sorted=True, frac=smoothness)
        return results[:, 1]

    punt_dist = punts.groupby('yrdline100')['net_punt_dist'].mean().to_frame()
    punt_dist.columns = ['rExpNetPuntDist']  # Update column names

    punt_dist['rExpNetPuntDist'].fillna(method = 'bfill', inplace = True)
    punt_dist['ExpNetPuntDist'] = curve_fit(
    punt_dist['rExpNetPuntDist'].index, punt_dist['rExpNetPuntDist'])

    exp_net_punt_dist_model_f = punt_dist['ExpNetPuntDist']


    return exp_net_punt_dist_model_f