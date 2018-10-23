import pandas as pd
import numpy as np

def extract_kickoffs_and_possessions(pxp):
    
    ko_mask = pxp['type'].isin(['Kickoff', 'Kickoff Return (Defense)','Kickoff Return Touchdown','Kickoff Return (Offense)'])  
    kickoffs = pxp.loc[ko_mask]
    # Exclude kickoffs and XPs and groupby GameID and Drive
    xp_mask = pxp['type'].isin(['Extra Point Good','Blocked PAT','Extra Point Missed','No Play'])
    game_drives = pxp.loc[~ko_mask & ~xp_mask].groupby(['gameId', 'driveIndex'])

    poss_starts = game_drives.head(1)

    # Concatenate kickoffs and first plays, sort, and reindex
    ko_and_poss = pd.concat([kickoffs, poss_starts])\
            .sort_values(['gameId', 'driveIndex', 'index'], na_position='first')
    ko_and_poss.reset_index(drop=True, inplace=True)

    # Extract game halves
    game_halves = ko_and_poss.groupby(['gameId', 'half'])
    # Compute changes in the scores.  + for Home and - for Away. Aka if the away team score then -7
    score_change = game_halves['homeScore'].diff() - game_halves['awayScore'].diff()
    ko_and_poss['score_change'] = score_change
    # Backfill the score change so that each possession now has a value for next score in the game (when does the next score come)
    ko_and_poss['NextScore'] = score_change.fillna(0).replace(to_replace=0., method='bfill')
#     ko_and_poss.loc[ko_and_poss['Touchdown']==1, 'NextScore'] = ko_and_poss['NextScore']/ko_and_poss['NextScore']*7
    
    # Determine if the possessing team is home or away
    posteam = ko_and_poss['offenseTeam']
    hometeam = ko_and_poss['homeTeam']
    awayteam = ko_and_poss['awayTeam']
    ko_and_poss['posteam_is_home'] = (posteam == hometeam).astype(int)
    ko_and_poss['posteam_is_away'] = (posteam == awayteam).astype(int)
    # NextScore is unchanged if posteam == hometeam and negated if posteam == awayteam
    ko_and_poss['PossessionValue'] = ko_and_poss['NextScore'] * \
        (ko_and_poss['posteam_is_home'] - ko_and_poss['posteam_is_away'])

    return ko_and_poss