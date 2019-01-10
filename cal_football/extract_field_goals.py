import pandas as pd

def extract_field_goals(pxp):
    fg_mask = pxp['type'].isin(['Field Goal Good','Field Goal Missed','Blocked Field Goal','Blocked Field Goal Touchdown',
                           'Missed Field Goal Return','Missed Field Goal Return Touchdown'])
    fgs = pxp.loc[fg_mask, ['FieldGoalDistance', 'FieldGoalResult']].copy()
    fgs['FieldGoalSuccess'] = (fgs['FieldGoalResult'] == 'Good').astype(int)
    return fgs
