import pandas as pd
import numpy as np
def create_final_output(pxp, conv_pxp):
    writer = pd.ExcelWriter('final_output.xlsx')
    for x in np.arange(1, 10):
        temp = pd.concat([pxp[pxp.yrdstogo == x], conv_pxp[pxp.yrdstogo == x]], axis=1).drop("yrdstogo", axis=1)
        temp['Notes'] = pd.Series()

        suggestions = []

        for index, row in temp.iterrows():
            if max(row.gfi_epv, row.fg_epv, row.punt_epv) == row.gfi_epv:
                suggestions.append("Go")
            if max(row.gfi_epv, row.fg_epv, row.punt_epv) == row.fg_epv:
                suggestions.append("Field Goal")
            if max(row.gfi_epv, row.fg_epv, row.punt_epv) == row.punt_epv:
                suggestions.append("Punt")

        temp['Suggested Decision'] = suggestions
        temp['avg_conv'] = pd.read_csv('./avg_conv_pct.csv')
        temp['mod_conv'] = pd.read_csv('./mod_conv_pct.csv')
        temp.to_excel(writer, '4th and ' + str(x), index=False)
    writer.save()
