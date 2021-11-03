import sys
sys.path.insert(1, 'C:\OIInsightsFramework')
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from datetime import datetime
from HANAFunctions import HANAFunctions
from SQLFunctions import SQLFunctions
import Config as con

def main():

    dateToDay = datetime.now()
    year, week_num, day_of_week = dateToDay.isocalendar()

    Cal_Week = str(year)+str(week_num-1)

    OBJ_HanaFuntions = HANAFunctions(user='*****', pwd='*****')

    dfHana = OBJ_HanaFuntions.execute_query_HANA(
        con.QUERY_MFG_HANA, [Cal_Week, Cal_Week])

    OBJ_SQLFuntions = SQLFunctions(con.CONN)

    #Delete existing records
    delEHS = con.DELETE_STATEMENT_EHS
    arg = [Cal_Week]
    OBJ_SQLFuntions.execute_statement_SQL(delEHS, arg)

    delMfg = con.DELETE_STATEMENT_MFG 
    arg = [Cal_Week]
    OBJ_SQLFuntions.execute_statement_SQL(delMfg, arg)

    delPlants = con.DELETE_STATEMENT_PLANTS 
    arg = [Cal_Week]
    OBJ_SQLFuntions.execute_statement_SQL(delPlants, arg)

    delQuality = con.DELETE_STATEMENT_QUA 
    arg = [Cal_Week]
    OBJ_SQLFuntions.execute_statement_SQL(delQuality, arg)

    df_geography = OBJ_SQLFuntions.execute_query_SQL(con.QUERY_GEOGRAPHY)

    df_Hana_Join_Geo = pd.merge(left=dfHana, right=df_geography[[
                                'Plant', 'CountryGroup']], on='Plant', how='left')

    df_Hana_Join_Geo = df_Hana_Join_Geo.fillna(0)


    for index, row in df_Hana_Join_Geo.iterrows():
        statement = con.INSERT_STATEMENT_MFG
        arg = [
            row['Week'], row['CountryGroup'], row['Plant'], row['PTP'], row['PTPS'], '', row['DownTime'], row['Downtime_Hours'], row['Hours_per_week']]
        OBJ_SQLFuntions.execute_statement_SQL(statement, arg)

    dfHeldware = OBJ_HanaFuntions.execute_query_HANA(
        con.QUERY_HELDWARE_HANA)

    df_Held_Join_Geo = pd.merge(left=dfHeldware, right=df_geography,
                                left_on='plant_code', right_on='PlantCode', how='inner')

    dfSeverity = OBJ_HanaFuntions.execute_query_HANA(
        con.QUERY_SEVERITY_HANA, [])

    if len(dfSeverity) > 0:
        df_pivotSeverity = dfSeverity.pivot_table(index=['calweek', 'plant_code'], columns=[
                                                'Severity'], values='count_notifications').fillna(0).reset_index()
    else:
        df_pivotSeverity = pd.DataFrame(columns=[
                                        'calweek', 'plant_code', '3- Significant', '4- Major', '5 - Critical Defect', 'count_notifications'])


    def create_column(df, column_name):
        df[column_name] = 0.0


    None if '3- Significant' in df_pivotSeverity.columns else create_column(
        df_pivotSeverity, '3- Significant')

    None if '4- Major' in df_pivotSeverity.columns else create_column(
        df_pivotSeverity, '4- Major')

    None if '5 - Critical Defect' in df_pivotSeverity.columns else create_column(
        df_pivotSeverity, '5 - Critical Defect')

    df_Held_Join_Sev = pd.merge(left=df_Held_Join_Geo, right=df_pivotSeverity, on=[
                                'calweek', 'plant_code'], how='left').fillna(0.0)

    df_Held_Join_Sev["prodution_heldware"] = pd.to_numeric(df_Held_Join_Sev["prodution_heldware"], downcast="float")
    df_Held_Join_Sev["total_heldware"] = pd.to_numeric(df_Held_Join_Sev["total_heldware"], downcast="float")
    df_Held_Join_Sev["held_inventory"] = pd.to_numeric(df_Held_Join_Sev["held_inventory"], downcast="float")

    df_held_grouped = df_Held_Join_Sev.groupby(['calweek', 'CountryGroup']).agg(
        {'prodution_heldware': 'sum',
        'total_heldware': 'sum',
        'held_inventory': 'sum',
        '3- Significant': 'sum',
        '4- Major': 'sum',
        '5 - Critical Defect': 'sum'
        }).reset_index()
        
    df_held_grouped['held_gen_percent'] = ((
        df_held_grouped['total_heldware']/df_held_grouped['prodution_heldware']).replace([np.inf, -np.inf], np.nan).fillna(0).astype(float).round(4))*100
    for index, row in df_held_grouped.iterrows():
        statement = con.INSERT_STATEMENT_QUALITY
        args = [
            row['calweek'], row['CountryGroup'], row['held_inventory'], '', row['total_heldware'], row['held_gen_percent'],
            row['3- Significant'], row['4- Major'], row['5 - Critical Defect'], '', '', '', row['prodution_heldware']]
        OBJ_SQLFuntions.execute_statement_SQL(statement, args)


if __name__ == '__main__':
    main()