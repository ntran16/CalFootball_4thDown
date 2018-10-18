import pandas as pd
import numpy as np
import cal_football as cf

def exp_fg_prob_model(fgs):

	def curve_fit(x, y, smoothness=.5):
		from statsmodels.nonparametric.smoothers_lowess import lowess
		results = lowess(y, x, is_sorted=True, frac=smoothness)
		return results[:, 1]

	fg_prob = fgs.groupby('FieldGoalDistance')['FieldGoalSuccess'].mean().to_frame()
	fg_prob.columns = ['rFieldGoalProb']  # Update column names
	under_63_mask = fg_prob.index <= 63.
	fg_under_63 = fg_prob.loc[under_63_mask]

	fg_prob.loc[under_63_mask, 'ExpFieldGoalProb'] = curve_fit(fg_under_63.index, fg_under_63['rFieldGoalProb'])

	exp_fg_prob_model_f = fg_prob.loc[under_63_mask, 'ExpFieldGoalProb'].copy()

	return exp_fg_prob_model_f