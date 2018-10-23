import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

def epv_model(pxp):
	extract_kickoffs_and_possessions(pxp)
	first_and_third_qtr = (ko_and_poss['quarter'] == 1) | (ko_and_poss['quarter'] == 3)
	ko_and_poss_first_and_third = ko_and_poss.loc[first_and_third_qtr]

	ko = ko_and_poss_first_and_third['type'].isin(['Kickoff'])
	ko_nonzero = ~(ko_and_poss_first_and_third['score_change']==0)
	# Compute the average kickoff value
	ekv = ko_and_poss_first_and_third.loc[ko_nonzero]['PossessionValue'].mean()

	pd.set_option('display.max_column', 100)
	# ekv = -1

	possession_values = ko_and_poss_first_and_third.loc[~ko].\
	    groupby('yrdline100')['PossessionValue'].\
	    mean().\
	    to_frame()

	possession_values.columns = ['rEPV']

	formula = 'rEPV ~ yrdline100'
	results = smf.ols(formula, data=possession_values.reset_index()).fit()
# print(results.summary())
	
	ekv = -.6

	possession_values['EPV'] = results.fittedvalues.values
	epv_model = possession_values['EPV']


	return ekv, epv_model
