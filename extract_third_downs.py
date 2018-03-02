import pandas as pd

def extract_third_downs(pxp):

    ignore_plays = ['Penalty', 'Timeout', 'End Period', 'Punt Return', 'No Play',
                   'Blocked Punt','Blocked Field Goal', 'Blocked Punt Touchdown', 'Punt',
                   'Field Goal Good', 'Field Goal Missed','Kickoff Return Touchdown',
                   'Kickoff Return (Offense)', 'Missed Field Goal Return',
                   'Defensive 2pt Conversion', 'Kickoff']
    ignore_plays_mask = pxp['type'].isin(ignore_plays)
    all_third_downs_mask = (pxp['down'] == 3)
    under_10_to_go = ((pxp['distance'] <= 9)&(pxp['distance'] >=0))
    third_down_mask = all_third_downs_mask & ~ignore_plays_mask & under_10_to_go

    third_down_plays = pxp.loc[third_down_mask].\
        copy().\
        reset_index(drop=True)
    return third_down_plays