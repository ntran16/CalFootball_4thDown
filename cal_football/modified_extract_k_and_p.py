import pandas as pd
import numpy as np

def modified_extract_k_and_p(pxp):
    
    
    ko_mask = pxp['type'].isin(['Kickoff', 'Kickoff Return (Defense)','Kickoff Return Touchdown','Kickoff Return (Offense)'])  
    kickoffs = pxp.loc[ko_mask]
    # Exclude kickoffs and XPs and groupby GameID and Drive
    xp_mask = pxp['type'].isin(['Extra Point Good','Blocked PAT','Extra Point Missed','No Play'])
    game_drives = pxp.loc[~ko_mask & ~xp_mask].groupby(['gameId', 'driveIndex'])

    poss_starts = game_drives.head(1)
    
    home_off_away_def = pxp["home_off_away_def"]

    # Concatenate kickoffs and first plays, sort, and reindex
    ko_and_poss = pd.concat([kickoffs, poss_starts, home_off_away_def])\
            .sort_values(['gameId', 'driveIndex', 'index'], na_position='first')
    ko_and_poss.reset_index(drop=True, inplace=True)

    # Extract game halves
    game_halves = ko_and_poss.groupby(['gameId', 'half'])
    
    #Original Score_change explanaition:
    # Compute changes in the scores.  + for Home and - for Away. Aka if the away team score then -7
    
    #Modified: Negative score change if team analogous to Cal's opponent scores. Postitive if team analagous to Cal scores
    #See n_most_similar most_similar() function for explaination as to what matchup_list[3] is.
    score_change = game_halves['homeScore'].diff() - game_halves['awayScore'].diff()
    score_change_arr = []
    ko_and_poss['unfinalized_sc'] = score_change
    # Backfill the score change so that each 
    
    for index, row in ko_and_poss.iterrows():
        if row["home_off_away_def"]:
            score_change_arr.append(row['unfinalized_sc'])
        else:
            score_change_arr.append(-row['unfinalized_sc'])
    ko_and_poss['score_change'] = score_change_arr
    ko_and_poss['NextScore'] = score_change.fillna(0).replace(to_replace=0., method='bfill')
    ko_and_poss.loc[ko_and_poss['Touchdown']==1, 'NextScore'] = ko_and_poss['NextScore']/ko_and_poss['NextScore']*7
    
    #originial algorithm:
    # Determine if the possessing team is home or away
    # NextScore is unchanged if posteam == hometeam and negated if posteam == awayteam
    
    #Matchup Modified Algorithm:
    #Determine if the posessing team is analagous to Cal or analgous to opponent team
    #NextScore is unchanged if posteam == ANALAGOUSCAL and negated if posteam == ANALGOUSOPP
    
    posteam_is_CAL_arr = []
    posteam_is_OPP_arr = []
    for index, row in ko_and_poss.iterrows():
        if row["home_off_away_def"]:
            posteam_is_CAL_arr.append(int(row['offenseTeam'] == row['homeTeam']))
            posteam_is_OPP_arr.append(int(row['offenseTeam'] == row['awayTeam']))
        else:
            posteam_is_CAL_arr.append(int(row['offenseTeam'] == row['awayTeam']))
            posteam_is_OPP_arr.append(int(row['offenseTeam'] == row['homeTeam']))
     
    ko_and_poss['posteam_is_CAL'] = posteam_is_CAL_arr
    ko_and_poss['posteam_is_OPP'] = posteam_is_OPP_arr
    ko_and_poss['PossessionValue'] = ko_and_poss['NextScore'] * \
        (ko_and_poss['posteam_is_CAL'] - ko_and_poss['posteam_is_OPP'])

    return ko_and_poss