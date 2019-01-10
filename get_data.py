"""
Argument:
    entries - can be one of "all", "Pac12", or the full name of any team as a string.

Returns: pandas data frame of specified data

"""
import pandas as pd
import numpy as np
import os.path as checkPath


def get_data(entries):
    data = []
    weeks_2017 = []
    for x in np.arange(1, 14):
        file = "./NCAA-Football-Data/2017PXP/PBP - 2017 - Week " + str(x) +".csv"
        if (checkPath.isfile(file)):
            weeks_2017.append(pd.read_csv(file))
    data_2017 = pd.concat(weeks_2017)

    weeks_2016 = []
    for x in np.arange(1, 16):
        weeks_2016.append(pd.read_csv("./NCAA-Football-Data/2016PXP/PBP - 2016 - Week " + str(x) +".csv"))
    data_2016 = pd.concat(weeks_2016)

    weeks_2015 = []
    for x in np.arange(1, 16):
        weeks_2015.append(pd.read_csv("./NCAA-Football-Data/2015PXP/PBP - 2015 - Week " + str(x) +".csv"))
    data_2015 = pd.concat(weeks_2015)

    weeks_2013 = []
    for x in np.arange(1, 16):
        weeks_2013.append(pd.read_csv("./NCAA-Football-Data/2013PXP/PBP - 2013 - Week " + str(x) +".csv"))
    data_2013 = pd.concat(weeks_2013)

    weeks_2012 = []
    for x in np.arange(1, 16):
        weeks_2012.append(pd.read_csv("./NCAA-Football-Data/2012PXP/PBP - 2012 - Week " + str(x) +".csv"))
    data_2012 = pd.concat(weeks_2012)

    weeks_2011 = []
    for x in np.arange(1, 16):
        weeks_2011.append(pd.read_csv("./NCAA-Football-Data/2011PXP/PBP - 2011 - Week " + str(x) +".csv"))
    data_2011 = pd.concat(weeks_2011)

    weeks_2010 = []
    for x in np.arange(1, 16):
        weeks_2010.append(pd.read_csv("./NCAA-Football-Data/2010PXP/PBP - 2010 - Week " + str(x) +".csv"))
    data_2010 = pd.concat(weeks_2010)

    weeks_2009 = []
    for x in np.arange(1, 16):
        weeks_2009.append(pd.read_csv("./NCAA-Football-Data/2009PXP/PBP - 2009 - Week " + str(x) +".csv"))
    data_2009 = pd.concat(weeks_2009)

    weeks_2008 = []
    for x in np.arange(1, 16):
        weeks_2008.append(pd.read_csv("./NCAA-Football-Data/2008PXP/PBP - 2008 - Week " + str(x) +".csv"))
    data_2008 = pd.concat(weeks_2008)

    weeks_2007 = []
    for x in np.arange(1, 15):
        weeks_2007.append(pd.read_csv("./NCAA-Football-Data/2007PXP/PBP - 2007 - Week " + str(x) +".csv"))
    data_2007 = pd.concat(weeks_2007)

    weeks_2006 = []
    for x in np.arange(1, 15):
        weeks_2006.append(pd.read_csv("./NCAA-Football-Data/2006PXP/PBP - 2006 - Week " + str(x) +".csv"))
    data_2006 = pd.concat(weeks_2006)

    weeks_2005 = []
    for x in np.arange(1, 15):
        weeks_2005.append(pd.read_csv("./NCAA-Football-Data/2005PXP/PBP - 2005 - Week " + str(x) +".csv"))
    data_2005 = pd.concat(weeks_2005)

    weeks_2004 = []
    for x in np.arange(1, 16):
        weeks_2004.append(pd.read_csv("./NCAA-Football-Data/2004PXP/PBP - 2004 - Week " + str(x) +".csv"))
    data_2004 = pd.concat(weeks_2004)

    weeks_2003 = []
    for x in np.arange(1, 17):
        weeks_2003.append(pd.read_csv("./NCAA-Football-Data/2003PXP/PBP - 2003 - Week " + str(x) +".csv"))
    data_2003 = pd.concat(weeks_2003)

    weeks_2002 = []
    for x in np.array([3, 6, 7, 9]):
        weeks_2002.append(pd.read_csv("./NCAA-Football-Data/2002PXP/PBP - 2002 - Week " + str(x) +".csv"))
    data_2002 = pd.concat(weeks_2002)

    weeks_2001 = []
    for x in list(np.array([1, 2, 3])) + list(np.arange(5, 9)) + list(np.arange(10, 17)):
        weeks_2001.append(pd.read_csv("./NCAA-Football-Data/2001PXP/PBP - 2001 - Week " + str(x) +".csv"))
    data_2001 = pd.concat(weeks_2001)

    data_2001_to_2017 = []

    for x in np.arange(2001, 2018):
        if x != 2014:
            data_2001_to_2017.append(locals()["data_" + str(x)])
    data = pd.concat(data_2001_to_2017)

    if entries == "all":
        data = pd.concat(data_2001_to_2017)
        return data
    if entries == "pac12":
        pac_12_team_names = ["Arizona State", "Arizona", "Cal", "Colorado", "Oregon", "Oregon State", "Stanford", "UCLA", "USC", "Utah", "Washington", "Washington St" ]
        data = data.loc[(data.awayTeam.isin(pac_12_team_names)) & (data.homeTeam.isin(pac_12_team_names))]
        return data
    else:
        if entries in data.homeTeam.unique() or entries in data.awayTeam.unique():
            home = data.loc[data.homeTeam == entries]
            away = data.loc[data.awayTeam == entries]
            data = pd.concat([home, away])
            return data
        else:
            print("Error! Please Enter a Valid Input")
            return None

    return pxp
