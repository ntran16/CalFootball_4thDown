def extract_fourth_downs(pxp):
    ignore_plays = ['Penalty', 'Timeout', 'End Period', 'Punt Return', 'No Play',
                   'Blocked Punt','Blocked Field Goal', 'Blocked Punt Touchdown', 'Punt',
                   'Field Goal Good', 'Field Goal Missed','Kickoff Return Touchdown',
                   'Kickoff Return (Offense)', 'Missed Field Goal Return',
                   'Defensive 2pt Conversion', 'Kickoff', 'Field Goal','Timeout']
    ignore_plays_mask4 = pxp['type'].isin(ignore_plays)
    all_fourth_downs_mask = (pxp['down'] == 4)
    under_10_to_go4 = ((pxp['distance'] <= 9)&(pxp['distance'] >=0))
    #team_mask = (pxp['homeAbbr'] == 'CAL') | (pxp['awayAbbr'] == 'CAL')
    fourth_down_mask = all_fourth_downs_mask & ~ignore_plays_mask4 & under_10_to_go4 #& team_mask

    fourth_down_plays = pxp.loc[fourth_down_mask].\
        copy().\
        reset_index(drop=True)
    return fourth_down_plays