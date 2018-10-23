import pandas as pd
import numpy as np
import cal_football as cf
import statsmodels.formula.api as smf

def exp_conv_pct_model(third_downs):
	def curve_fit(x, y, smoothness=.5):
		from statsmodels.nonparametric.smoothers_lowess import lowess
		results = lowess(y, x, is_sorted=True, frac=smoothness)
		return results[:, 1]

	conv_pct = third_downs.groupby(['yrdregion', 'distance'])['1stdownconversion'].mean().to_frame()
	conv_pct.columns = ['rConvPct']  # update column names

	for region in ['Inside10', '10to20', 'Beyond20']:
		conv_pct_region = conv_pct.loc[region]
		conv_pct.loc[region, 'ExpConvPct'] = curve_fit(conv_pct_region.index, conv_pct_region['rConvPct'])

		exp_conv_pct_model_f = conv_pct['ExpConvPct']

	return exp_conv_pct_model_f