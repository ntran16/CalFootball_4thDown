import csv
import os
import glob
import numpy as np
import pandas as pd

def addResults(pxp):
	pxp['Touchdown'] = np.where((pxp['type'].notnull()) & (pxp['type'].str.contains('Touchdown', case = False)), 1, 0)
	pxp['ExPointResult'] = np.select([pxp['type'] == 'Extra Point Good', pxp['type'] == 'Extra Point Missed', pxp['type'] == 'Blocked PAT'], ['Made', 'Missed', 'Missed PAT'], default = np.nan)
	# TODO pxp['TwoPointConv']
	pxp['Safety'] = np.where((pxp['type'].notnull()) & pxp['type'].str.contains('Safety', case = False), 1, 0)
	pxp['FieldGoalResult'] = np.select([pxp['type'] == 'Field Goal Good', pxp['type'] == 'Field Goal Missed', 
										pxp['type'] == 'Missed Field Goal Return', pxp['type'] == 'Missed Field Goal Return Touchdown',
										pxp['type'] == 'Blocked Field Goal', pxp['type'] == 'Blocked Field Goal Touchdown'], 
										['Made', 'Missed', 'Missed', 'Missed', 'Missed', 'Missed'], default = np.nan)

	notreturned = pxp['type'].isin(['Field Goal Good', 'Field Goal Missed'])
	notretmatch = pxp.loc[notreturned]

	pxp.loc[notreturned, 'FieldGoalDistance'] = notretmatch['yardsGained']

	returned = pxp['type'].isin(['Missed Field Goal Return', 'Missed Field Goal Return Touchdown','Blocked Field Goal Touchdown', 'Blocked Field Goal'])
	retmatch = pxp.loc[returned]

	pxp.loc[returned, 'FieldGoalDistance'] = retmatch['yardLine'].astype(int) + 17

	wrongdistance = pxp['FieldGoalDistance'] == 0
	wrongmatch = pxp.loc[wrongdistance]

	pxp.loc[wrongdistance, 'FieldGoalDistance'] = wrongmatch['yardLine'].astype(int) + 17
	#TODO Fix field goal success

def distanceBasedOnDescription(description):
	words = description.split(' ')
	for i in range(1, len(words)):
		if i < 
		if words[i] == 'yard'

def fixFieldGoalDistance(pxp):
	fieldgoalnodistance = (pxp['type'] == 'Field Goal') & (~pxp['FieldGoalDistance'].notnull())
	nodistancematch = pxp.loc[fieldgoalnodistance]

	pxp.loc[fieldgoalnodistance, 'FieldGoalDistance'] = nodistancematch['yardsGained']

def fixFieldGoalResult(pxp):
	pxp.loc[(pxp['type'] == 'Field Goal') & (pxp['description'].str.contains('no good', case = False)), 'FieldGoalResult'] = 'Missed'
	pxp.loc[(pxp['type'] == 'Field Goal') & (pxp['description'].str.contains('MISSED', case = False)), 'FieldGoalResult'] = 'Missed'
	pxp.loc[(pxp['type'] == 'Field Goal') & (pxp['description'].str.contains('is good', case = False)), 'FieldGoalResult'] = 'Made'
	pxp.loc[(pxp['type'] == 'Field Goal') & (pxp['description'].str.contains('field goal GOOD', case = False)), 'FieldGoalResult'] = 'Made'

def replaceTypes(pxp):
	pxp['type'] = pxp['type'].replace(['Kickoff Return (Offense)', 'Kickoff Return Touchdown', 'Kickoff Return (Defense)'], 'Kickoff')
	pxp['type'] = pxp['type'].replace(['Pass Completion', 'Pass Incompletion', 'Pass Interception', 'Two Point Pass', 'Interception Return Touchdown', 
		'Pass Reception', 'Pass Interception Return', 'Passing Touchdown', 'Interception'], 'Pass')
	pxp['type'] = pxp['type'].replace(['Rush', 'Two Point Rush', 'Rushing Touchdown'], 'Rush')
	pxp['type'] = pxp['type'].replace(['Punt Return', 'Blocked Punt Touchdown', 'Blocked Punt', 'Punt Return Touchdown'], 'Punt')
	pxp['type'] = pxp['type'].replace(['Penalty', 'End Period'], 'No Play')
	pxp['type'] = pxp['type'].replace(['Offensive 1pt Safety'], 'Safety')
	pxp['type'] = pxp['type'].replace(['Blocked Field Goal Touchdown', 'Blocked Field Goal', 'Missed Field Goal Return Touchdown', 
		'Field Goal Missed', 'Field Goal Good', 'Missed Field Goal Return'], 'Field Goal')
	pxp['type'] = pxp['type'].replace(['Blocked PAT', 'Extra Point Good', 'Extra Point Missed'], 'Extra Point')
	pxp['type'] = pxp['type'].replace(['End of Half'], 'Quarter End')

def fixFieldGoal(pxp):
	pxp.loc[(pxp['description'].notnull()) & (pxp['description'].str.contains('field goal', case = False)) 
	& (pxp['type'] != 'Field Goal') & (pxp['description'].str.contains('MISSED', case = False)), 'type'] = 'Field Goal'

	pxp.loc[(pxp['description'].notnull()) & (pxp['description'].str.contains('field goal', case = False)) 
	& (pxp['type'] != 'Field Goal') & (pxp['description'].str.contains('GOOD', case = False)), 'type'] = 'Field Goal'

	pxp.loc[(pxp['description'].notnull()) & (pxp['description'].str.contains('field goal', case = False)) 
	& (pxp['type'] != 'Field Goal') & (pxp['description'].str.contains('BLOCKED', case = False)), 'type'] = 'Field Goal'

	pxp.loc[(pxp['description'].notnull()) & (pxp['type'] == 'Field Goal') & (pxp['description'].str.contains('NO PLAY', case = False)), 'type'] = 'No Play'

def fixKickoff(pxp):
	pxp.loc[(pxp['description'].notnull()) & (pxp['description'].str.contains('Kickoff', case = False)) 
	& (pxp['type'] == 'Safety'), 'type'] = 'Kickoff'
	pxp.loc[(pxp['description'].notnull()) & (pxp['description'].str.contains('Kickoff', case = False)) 
	& (pxp['type'] == 'Extra Point'), 'type'] = 'Kickoff'
	pxp.loc[(pxp['description'].notnull()) & (pxp['description'].str.contains('Kickoff', case = False)) 
	& (pxp['type'] == 'Punt'), 'type'] = 'Kickoff'

def fixYardLine(pxp):
	mask = (pxp['offenseTeam'] == pxp['homeTeam']) & (~pxp['description'].str.contains('kickoff', case = False, na = True))
	matching = pxp.loc[mask]

	pxp.loc[mask, 'yardLine'] = 100 - matching['yardLine']


try:
	os.makedirs('Improved-NCAA-Football-Data')
except:
	pass

for year in range(2001, 2018):
	files = glob.glob('NCAA-Football-Data/{}PXP/*.csv'.format(year))
	try:
		os.makedirs('Improved-NCAA-Football-Data/{}PXP'.format(year))
	except:
		pass

	for file in files:
		print(os.path.basename(file))
		skip_column = ['endYardLine']
		plays = pd.read_csv(file, usecols = lambda x: x not in skip_column)
		fileName = 'Improved-NCAA-Football-Data/{}PXP'.format(year) + '/' + os.path.basename(file)
		fixYardLine(plays)
		addResults(plays)
		replaceTypes(plays)
		fixFieldGoal(plays)
		fixFieldGoalDistance(plays)
		fixKickoff(plays)
		fixFieldGoalResult(plays)
		plays.to_csv(fileName, index=False)