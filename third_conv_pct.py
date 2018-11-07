def third_conv_pct(pxp):
    # get thirddow data
    third_downs = extract_third_downs(pxp)
    ignore_plays = ['Penalty', 'End Period', 'Timeout', 'End of Half', 'End of Game',
                    'No Play', 'Coin Toss', 'Extra Point Good', 'Blocked PAT', 'Extra Point Missed']

    ignore_mask = ~pxp['type'].isin(ignore_plays)
    game_halves = pxp. \
        loc[ignore_mask]. \
        groupby(['gameId', 'half'])
    pxp.loc[ignore_mask, 'nextposteam'] = game_halves['offenseTeam']. \
        shift(-1). \
        fillna(method='bfill')
    pxp.loc[ignore_mask, 'nextyrdline100'] = game_halves['yrdline100']. \
        shift(-1). \
        fillna(method='bfill')
    pxp.loc[ignore_mask, 'nextdown'] = game_halves['down']. \
        shift(-1). \
        fillna(method='bfill')
    pxp.loc[ignore_mask, '1stdownconversion'] = (
            (pxp.loc[ignore_mask, 'nextdown'] == 1.) |
            (pxp.loc[ignore_mask, 'distance'] <= pxp.loc[ignore_mask, 'yardsGained']) |
            (pxp.loc[ignore_mask, 'Touchdown'] == 1)
    ).astype(int)

    pxp['yrdregion'] = pd.cut(pxp['yrdline100'], [0., 9., 19., 29., 39., 49., 59., 69., 79., 89., 100.],
                              labels=['Inside10', '10to20', '20to30', '30to40', '40to50', '50to60', '60to70', '70to80',
                                      '80to90', 'AndGoal'])

    # set display option
    pd.set_option('display.max_rows', 1000)

    conv_pct3 = third_downs. \
        groupby(['yrdregion', 'distance'])['1stdownconversion']. \
        mean(). \
        to_frame()
    conv_pct3.columns = ['rConvPct3']  # update column names

    count3 = third_downs. \
        groupby(['yrdregion', 'distance'])['1stdownconversion']. \
        size(). \
        to_frame()
    count3.columns = ['count']  # update column names

    result = pd.concat([conv_pct3, count3], axis=1)
    a = [result.columns.tolist()] + result.reset_index().values.tolist()

    return a