import pandas as pd
import numpy as np

import pandas as pd

def extract_punts(pxp):

    # Build table of punts
    punt_mask = pxp['type'].isin(['Punt', 'Blocked Punt', 'Punt Return'])
    punts = pxp.loc[punt_mask].copy()
    punts.reset_index(drop=True, inplace=True)

    # Extract relevant values
    posteam = punts['offenseTeam']
    nextposteam = punts['nextposteam']
    yrdline = punts['yrdline100']
    nextyardline = punts['nextyrdline100'] 

    # Determine if there was a possession change, ie. the punt went off as expected.
    # This excludes muffs or fumbled returns.  It also exludes return TDs and probably
    # some other cases.  It is likely not too bad to do this since these events are rare.
    poss_change = (posteam != nextposteam)
    # Determine the net punt distance
    net_punt_dist = (yrdline.astype(int) - (100 - nextyardline.astype(int))) * poss_change.astype(int)
    # Add net punt length to punts table
    punts.loc[poss_change, 'net_punt_dist'] = net_punt_dist[poss_change]
    
    return punts