# Bootstrap Grid tutorial - adding style to the app
import sys
sys.path.insert(1,'C:\OIInsightsFramework')
import time
from datetime import datetime
import traceback

# -*- coding: utf-8 -*-
import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#import dash_table_experiments as dt
from dash.dependencies import Input, Output, State
from flask import request

import Config as con
from SQLFunctions import SQLFunctions

# Initialize data==================
dateToDay = datetime.now()
year, week_num, day_of_week = dateToDay.isocalendar()
Cal_Week = str(year) + str(week_num - 1)
Week_Number = str(week_num - 1)
print(Cal_Week)
print(Week_Number)
SqlFunction = SQLFunctions(con.CONN)
df_MFG_Plants = SqlFunction.execute_query_SQL(con.QUERY_ALL_PLANTS_WEEK,
                                              [Cal_Week])
print(df_MFG_Plants)
# =================================

# Filter queries===================


def filter_plants_by_CG(df, countrygroup):
    dff = df[df['CountryGroup'] == countrygroup]
    dff.reset_index(inplace=True)
    return dff


def filter_by_plants(df, plant):
    dff = df[df['Plant'] == plant].copy()
    dff.reset_index(inplace=True)
    return dff


# =================================

# SQL Queries=====================


# [Week],[CountryGroup],[HeldwareInventory],[QCQuantity],
# [QCSeverity],[CDQuantity],[Highlights],[HeldwareGeneration]
def insert_update_quality(week, countrygroup, qua_heldwareinventory, qua_Highlights,
                          qua_heldGenTO, qua_heldGenPercent,
                          qua_threeQuantity, qua_fourQuantity,
                          qua_fiveQuantity, qua_threeComments,
                          qua_fourComments, qua_fiveComments):

    try:
        df_quality = SqlFunction.execute_query_SQL(con.QUERY_QUALITY,
                                                   [week, countrygroup])
        if len(df_quality) == 0:
            print("Inserting quality data")
            statement = con.INSERT_STATEMENT_QUALITY
            args = [
                week, countrygroup, qua_heldwareinventory, qua_Highlights,
                qua_heldGenTO, qua_heldGenPercent, qua_threeQuantity, qua_fourQuantity,
                qua_fiveQuantity, qua_threeComments, qua_fourComments, qua_fiveComments
            ]
        else:
            print("Updating quality data")
            statement = con.UPDATE_STATEMENT_QUALITY
            args = [
                qua_heldwareinventory, qua_Highlights,
                qua_heldGenTO, qua_heldGenPercent,
                qua_threeQuantity, qua_fourQuantity,
                qua_fiveQuantity, qua_threeComments,
                qua_fourComments, qua_fiveComments, week, countrygroup
            ]
        print("Executing statement\n" + statement)
        result = SqlFunction.execute_statement_SQL(statement, args)
        return result
    except:
        print("Algo salió mal en insert_update_quality\n")
        traceback.print_stack()
        return 0


# [Week],[CountryGroup],[LTIQuantity],[MTIQuantity]
# [LTIDescription],[MTIDescription],[Highlights]
def insert_update_ehs(week, countrygroup, ltiquantity, mtiquantity,
                      ltidescription, mtidescription, highlights):
    try:
        df_ehs = SqlFunction.execute_query_SQL(con.QUERY_EHS,
                                               [week, countrygroup])
        if len(df_ehs) == 0:
            print("Inserting EHS data")
            statement = con.INSERT_STATEMENT_EHS
            args = [
                week, countrygroup, ltiquantity, mtiquantity, ltidescription,
                mtidescription, highlights
            ]
        else:
            print("Updating EHS data")
            statement = con.UPDATE_STATEMENT_EHS
            args = [
                ltiquantity, mtiquantity, ltidescription, mtidescription,
                highlights, week, countrygroup
            ]
        print("Executing statement\n" + statement)
        result = SqlFunction.execute_statement_SQL(statement, args)
        return result
    except:
        print("Algo salió mal en insert_update_ehs\n")
        traceback.print_stack()
        print(sys.exc_info())
        return 0


# [Week],[CountryGroup],[Highlights],[ProjectStatus],[Support]
def insert_update_manufacturing(week, countrygroup, highlights, projectstatus,
                                support):
    try:
        df_manufacturing = SqlFunction.execute_query_SQL(
            con.QUERY_MFG_MANUFACTURING, [week, countrygroup])
        if len(df_manufacturing) == 0:
            print("Inserting manufacturing data")
            statement = con.INSERT_STATEMENT_MANUFACTURING
            args = [week, countrygroup, highlights, projectstatus, support]
        else:
            print("Updating manufacturing data")
            statement = con.UPDATE_STATEMENT_MANUFACTURING
            args = [highlights, projectstatus, support, week, countrygroup]
        print("Executing statement\n" + statement)
        result = SqlFunction.execute_statement_SQL(statement, args)
        return result
    except:
        print("Algo salió mal en insert_update_manufacturing\n")
        traceback.print_stack()
        print(sys.exc_info())
        return 0


# [Week],[CountryGroup],[Plant],[PTP],[PTPS],[MainReason],[DownTime]
def insert_update_mfg_plants(week, countrygroup, plant, ptp, ptps, mainreason,
                             downtime):
    try:
        df_mfg_plant = SqlFunction.execute_query_SQL(
            con.QUERY_MFG_PLANT, [week, countrygroup, plant])
        if len(df_mfg_plant) == 0:
            print("Inserting Mfg_Plants data")
            statement = con.INSERT_STATEMENT_MFG
            args = [week, countrygroup, plant, ptp, ptps, mainreason, downtime]
        else:
            print("Updating Mfg_Plants data")
            statement = con.UPDATE_STATEMENT_MFG
            args = [ptp, ptps, mainreason, downtime, week, countrygroup, plant]
        print("Executing statement\n" + statement)
        result = SqlFunction.execute_statement_SQL(statement, args)
        return result
    except:
        print("Algo salió mal en insert_update_mfg_plants\n")
        traceback.print_stack()
        print(sys.exc_info())
        return 0


# =================================================

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

auth = dash_auth.BasicAuth(app, con.VALID_USERNAME_PASSWORD_PAIRS)

app.title = 'HIGHLIGHTS'


# Manufacturing builder===============
def build_manufacturing_section(df_plants, highlights, mfg_project_status):
    table_header_Mfg = [
        html.Thead(
            dbc.Row([
                dbc.Col("Week " + Week_Number + " Results", width=2,
                        className="font-weight-bold", style={'align-self': 'center'}),
                dbc.Col("PTP", width=1, className="font-weight-bold",
                        style={'align-self': 'center'}),
                dbc.Col("PTPS", width=1, className="font-weight-bold",
                        style={'align-self': 'center'}),
                dbc.Col("Unscheduled Downtime (%)", width=1,
                        className="font-weight-bold", style={'padding-left': '0', 'padding-right': '0','align-self': 'center'}),
                dbc.Col("Comments", className="font-weight-bold",
                        style={'padding-left': '0', 'padding-right': '0', 'align-self': 'center'})
            ],
                style={
                'backgroundColor': 'rgb(51, 102, 153)',
                "color": "white",
                'padding-right': '0',
                'padding-left': '0',
                'border-collapse': 'collapse',
                'margin': '0'
            }))
    ]

    Plant_1PTP = dbc.Input(id="Plant1PTP", value=2,
                           type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_1PTPS = dbc.Input(id="Plant1PTPS", value='',
                            type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_1MR = dbc.Textarea(id="Plant1mainReason", value="",
                           className="border-0", style={'height':'40px'})
    Plant_1DT = dbc.Input(id="Plant1downtime", value="", style={'text-align': 'center'},
                          type="number", className="border-0")
    Plant_2PTP = dbc.Input(id="Plant2PTP", value='',
                           type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_2PTPS = dbc.Input(id="Plant2PTPS", value='',
                            type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_2MR = dbc.Textarea(id="Plant2mainReason", value="",
                          className="border-0", style={'height':'40px'})
    Plant_2DT = dbc.Input(id="Plant2downtime", value="",
                          type="number", className="border-0", style={'text-align': 'center'}) 
    Plant_3PTP = dbc.Input(id="Plant3PTP", value='',
                           type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_3PTPS = dbc.Input(id="Plant3PTPS", value='',
                            type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_3MR = dbc.Textarea(id="Plant3mainReason", value="",
                           className="border-0",style={'height':'40px'})
    Plant_3DT = dbc.Input(id="Plant3downtime", value="",
                          type="number", className="border-0", style={'text-align': 'center'})
    Plant_4PTP = dbc.Input(id="Plant4PTP", value='',
                           type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_4PTPS = dbc.Input(id="Plant4PTPS", value='',
                            type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_4MR = dbc.Textarea(id="Plant4mainReason", value="",
                          className="border-0", style={'height':'40px'})
    Plant_4DT = dbc.Input(id="Plant4downtime", value="",
                          type="number", className="border-0", style={'text-align': 'center'})
    Plant_5PTP = dbc.Input(id="Plant5PTP", value='',
                           type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_5PTPS = dbc.Input(id="Plant5PTPS", value='',
                            type="number", min=0.00, max=100.00, step=0.01, className="border-0", style={'text-align': 'center'})
    Plant_5MR = dbc.Textarea(id="Plant5mainReason", value="",
                          className="border-0", style={'height':'40px'})
    Plant_5DT = dbc.Input(id="Plant5downtime", value="",
                          type="number", className="border-0", style={'text-align': 'center'})

    PlantOptions = [{
        'label': label,
        'value': label
    } for label in df_plants['Plant'].unique()]

    Plant1DD = dcc.Dropdown(
        id="Plant1DD", options=PlantOptions, style={"border": '0px','text-transform': 'unset !important'})
    Plant2DD = dcc.Dropdown(
        id="Plant2DD", options=PlantOptions, style={"border": '0px','text-transform': 'unset !important'})
    Plant3DD = dcc.Dropdown(
        id="Plant3DD", options=PlantOptions, style={"border": '0px','text-transform': 'unset !important'})
    Plant4DD = dcc.Dropdown(
        id="Plant4DD", options=PlantOptions, style={"border": '0px','text-transform': 'unset !important'})
    Plant5DD = dcc.Dropdown(
        id="Plant5DD", options=PlantOptions, style={"border": '0px','text-transform': 'unset !important'})

    row_style = {'border': '1px solid', 'border-color': 'lightgrey',
                 'padding-right': '0', 'padding-left': '0'}
    row1_Mfg = dbc.Row([
        dbc.Col(Plant1DD, width=2, style=row_style),
        dbc.Col(Plant_1PTP, width=1, style=row_style),
        dbc.Col(Plant_1PTPS, width=1, style=row_style),
        dbc.Col(Plant_1DT, width=1, style=row_style),
        dbc.Col(Plant_1MR, style=row_style),
    ], style={'margin': '0'})
    row2_Mfg = dbc.Row([
        dbc.Col(Plant2DD, width=2, style=row_style),
        dbc.Col(Plant_2PTP, width=1, style=row_style),
        dbc.Col(Plant_2PTPS, width=1, style=row_style),
        dbc.Col(Plant_2DT, width=1, style=row_style),
        dbc.Col(Plant_2MR, style=row_style),
    ], style={'margin': '0'})
    row3_Mfg = dbc.Row([
        dbc.Col(Plant3DD, width=2, style=row_style),
        dbc.Col(Plant_3PTP, width=1, style=row_style),
        dbc.Col(Plant_3PTPS, width=1, style=row_style),
        dbc.Col(Plant_3DT, width=1, style=row_style),
        dbc.Col(Plant_3MR, style=row_style),
    ], style={'margin': '0'})
    row4_Mfg = dbc.Row([
        dbc.Col(Plant4DD, width=2, style=row_style),
        dbc.Col(Plant_4PTP, width=1, style=row_style),
        dbc.Col(Plant_4PTPS, width=1, style=row_style),
        dbc.Col(Plant_4DT, width=1, style=row_style),
        dbc.Col(Plant_4MR, style=row_style),
    ], style={'margin': '0'})
    row5_Mfg = dbc.Row([
        dbc.Col(Plant5DD, width=2, style=row_style),
        dbc.Col(Plant_5PTP, width=1, style=row_style),
        dbc.Col(Plant_5PTPS, width=1, style=row_style),
        dbc.Col(Plant_5DT, width=1, style=row_style),
        dbc.Col(Plant_5MR, style=row_style),
    ], style={'margin': '0'})

    table_body = [
        html.Tbody([row1_Mfg, row2_Mfg, row3_Mfg, row4_Mfg, row5_Mfg])
    ]

    tableMFG = dbc.Table(
        table_header_Mfg + table_body,
        className='table text-center table-bordered table-hover cell cell-1-1',
        style={'maxWidth': '100%'})

    Mfg_HightLights_Input = dbc.FormGroup([
        html.H2('MANUFACTURING', className="text-secondary"),
        dbc.Label("Select up to 5 plants impacting performance:",
                  html_for="mfg_table"),
        dbc.Label("   ", html_for="Space2"),
        tableMFG,
        dbc.Label("Other Manufacturing Highlights", html_for="Mfg_HighLights"),
        dbc.Textarea(id="Mfg_HightLights",
                     placeholder="(victories & other comments)",
                     value=highlights),
        html.Div([dbc.Label("   ", html_for="Space3")],
                 style={'marginBottom': '1.5em'}),
        html.H3('MFG. PROJECTS STATUS', className="text-secondary"),
        html.Div([], style={"height": "15px"}),
        dbc.Textarea(id="Project_Status",
                     placeholder="Project/Comments",
                     style={"height": "105px"},
                     value=mfg_project_status),
        html.Div([dbc.Label("   ", html_for="Space3")],
                 style={'marginBottom': '1.5em'}),
        html.Div(style={'padding': '0px', 'border-style': 'solid',
                        'color': 'rgba(51, 102, 153)'}),
    ])

    formMFG = dbc.Form([Mfg_HightLights_Input])
    return formMFG


# ======================================


# Quality builder=====================
def build_quality_section(qua_heldwareinventory, qua_Highlights,
                          qua_heldGenTO, qua_heldGenPercent,
                          qua_threeQuantity, qua_fourQuantity,
                          qua_fiveQuantity, qua_threeComments,
                          qua_fourComments, qua_fiveComments):

    table_header_Held = [
        html.Thead(
            html.Tr([
                html.Th("Generation TO"),
                html.Th("Generation %"),
                html.Th("Inventory TO")
            ],
                style={
                'backgroundColor': 'rgb(51, 102, 153)',
                "color": "white",
                'margin': '0'
            }))
    ]

    table_header_Qua = [
        html.Thead(
            dbc.Row([
                dbc.Col("Severity", width=4, className="font-weight-bold"),
                dbc.Col("Qty", width=2, className="font-weight-bold",
                        style={'max-width': '12%', 'align-self': 'center', 'margin': 'auto'}),
                dbc.Col("Relevant Comments", className="font-weight-bold",
                        width=5, style={'align-self': 'center', 'margin': 'auto'})
            ],
                style={
                'backgroundColor': 'rgb(51, 102, 153)',
                "color": "white",
                'margin': '0'
            }))
    ]
    
    if (qua_heldGenTO>0.0):
        qua_heldGenTO= round(qua_heldGenTO,2)
    else:
        pass

    if (qua_heldGenPercent>0.0):
        qua_heldGenPercent= round(qua_heldGenPercent,2)
    else:
        pass

    if (qua_heldwareinventory>0):
        qua_heldwareinventory= round(qua_heldwareinventory,2)
    else:
        pass

    HeldWGenTO = dbc.Input(id="HeldW_GenTO",
                           placeholder="KT",
                           value=qua_heldGenTO,
                           type="number")
    HeldWGenPercent = dbc.Input(id="HeldW_Gen_Percent",
                                min=0.00, max=100.00, step=0.01,
                                placeholder="%",
                                value=qua_heldGenPercent,
                                type="number")
    HeldInventoryTO = dbc.Input(id="Inventory_TO",
                                placeholder="KT",
                                value=qua_heldwareinventory,
                                type="number")

    CompCritical = dbc.Label("5-Critical",
                             html_for="label_critical", className="border-0")
    CompMajor = dbc.Label("4-Major",
                          html_for="label_major", className="border-0")
    CompSignificant = dbc.Label("3-Significant",
                                html_for="label_significant", className="border-0")
    CompQtyFive = dbc.Input(id="Quantity_complaints5",
                            value=qua_fiveQuantity,
                            type="number",
                            className="border-0", style={'text-align': 'center'})
    CompQtyFour = dbc.Input(id="Quantity_complaints4",
                            value=qua_fourQuantity,
                            type="number",
                            className="border-0", style={'text-align': 'center'})
    CompQtyThree = dbc.Input(id="Quantity_complaints3",
                             value=qua_threeQuantity,
                             type="number",
                             className="border-0", style={'text-align': 'center'})
    CommentFive = dbc.Textarea(id="Comment_complaints5",
                            value=qua_fiveComments,
                            className="border-0",style={'height':'40px'})
    CommentFour = dbc.Textarea(id="Comment_complaints4",
                            value=qua_fourComments,
                            className="border-0",style={'height':'40px'})
    CommentThree = dbc.Textarea(id="Comment_complaints3",
                             value=qua_threeComments,
                             className="border-0",style={'height':'40px'})

    row_styleQ = {'border': '1px solid', 'border-color': 'lightgrey',
                  'padding-right': '0', 'padding-left': '0'}

    row1Held = html.Tr(
        [html.Td(HeldWGenTO),
         html.Td(HeldWGenPercent),
         html.Td(HeldInventoryTO)])

    row1Qua = dbc.Row(
        [dbc.Col(CompCritical, width=4, style=row_styleQ),
         dbc.Col(CompQtyFive, width=2, style=row_styleQ),
         dbc.Col(CommentFive, width=5,
                 style={'border': '1px solid',
                        'border-color': 'lightgrey',
                        'padding-right': '0',
                        'padding-left': '0',
                        'max-width': '50%',
                        'flex': 'auto'})
         ], style={'margin': '0'})

    row2Qua = dbc.Row(
        [dbc.Col(CompMajor, width=4, style=row_styleQ),
         dbc.Col(CompQtyFour, width=2, style=row_styleQ),
         dbc.Col(CommentFour, width=5,
                 style={'border': '1px solid',
                        'border-color': 'lightgrey',
                        'padding-right': '0',
                        'padding-left': '0',
                        'max-width': '50%',
                        'flex': 'auto'})
         ], style={'margin': '0'})

    row3Qua = dbc.Row(
        [dbc.Col(CompSignificant, width=4, style=row_styleQ),
         dbc.Col(CompQtyThree, width=2, style=row_styleQ),
         dbc.Col(CommentThree, width=5,
                 style={'border': '1px solid',
                        'border-color': 'lightgrey',
                        'padding-right': '0',
                        'padding-left': '0',
                        'max-width': '50%',
                        'flex': 'auto'})
         ], style={'margin': '0'})

    table_body_Held = [html.Tbody([row1Held])]
    table_body_Qua = [html.Tbody([row1Qua, row2Qua, row3Qua])]

    tableHeld = dbc.Table(table_header_Held + table_body_Held,
                          bordered=True,
                          className='table-sm text-center table-hover')

    tableQua = dbc.Table(table_header_Qua + table_body_Qua,
                         bordered=True,
                         className='table-sm text-center table-hover')

    Quality_Input = dbc.FormGroup([
        html.H2('Quality', className="text-secondary"),
        dbc.Label("   ", html_for="Space3"),
        dbc.Label("Heldware" + ' -W' + Week_Number,
                  html_for="Quality_Highlights"),
        tableHeld,
        dbc.Label("   ", html_for="Space3"),
        dbc.Label("Quality complaints" + ' -W' + Week_Number,
                  html_for="Quality_Highlights"),
        tableQua,
        dbc.Label("   ", html_for="Space3"),
        dbc.Label("Quality Highlights for the week",
                  html_for="Quality_Highlights"),
        dbc.Textarea(id="Qua_Highligths",
                     placeholder="(Revelant comments)",
                     className='form-control',
                     value=qua_Highlights),
    ])

    formQuality = dbc.Form([Quality_Input])
    return formQuality


# ======================================


# EHS builder=========================
def build_EHS_section(ehs_highlight, ltiquantity,
                      ltidescription, mtiquantity, mtidescription):
    table_header_EHS = [
        html.Thead(
            dbc.Row(
                [
                    dbc.Col("Recordable Incidents",
                            className="font-weight-bold", width=3),
                    dbc.Col("Quantity", className="font-weight-bold", width=2, style={
                        'max-width': '22%', 'align-self': 'center', 'margin': 'auto'
                    }),
                    dbc.Col("Short Description", className="font-weight-bold", width=5, style={
                        'align-self': 'center', 'margin': 'auto'
                    })
                ],
                style={
                    'backgroundColor': 'rgb(51, 102, 153)',
                    "color": "white",
                    'margin': '0'
                }))
    ]

    LTI_EHS_label = dbc.Label("LTI", html_for="LTI_EHS")
    LTI_Quantity = dbc.Input(id="LTI_Quantity",
                             value=ltiquantity,
                             type="number", className="border-0", style={'text-align': 'center'})
    LTI_Description = dbc.Textarea(id="LTI_Description",
                                value=ltidescription,
                                className="border-0", style={'height':'40px'})
    MTI_EHS_label = dbc.Label("MTI", html_for="LTI_EHS")
    MTI_Quantity = dbc.Input(id="MTI_Quantity",
                             value=mtiquantity,
                             type="number", className="border-0", style={'text-align': 'center'})
    MTI_Description = dbc.Textarea(id="MTI_Description",
                                   value=mtidescription, className="border-0", style={'height':'40px'})
    # className="border-0", type="text",

    row_styleH = {'border': '1px solid', 'border-color': 'lightgrey',
                  'padding-right': '0', 'padding-left': '0'}

    row1EHS = dbc.Row([
        dbc.Col(LTI_EHS_label, width=3, style=row_styleH),
        dbc.Col(LTI_Quantity, width=2,
                style={'border': '1px solid',
                       'border-color': 'lightgrey',
                       'padding-right': '0',
                       'padding-left': '0',
                       'max-width': '22%',
                       'flex': 'auto'}),
        dbc.Col(LTI_Description, width=6,
                style={'border': '1px solid',
                       'border-color': 'lightgrey',
                       'padding-right': '0',
                       'padding-left': '0',
                       'max-width': '53%',
                       'flex': 'auto'})
    ], style={'margin': '0'})

    row2EHS = dbc.Row([
        dbc.Col(MTI_EHS_label, width=3, style=row_styleH),
        dbc.Col(MTI_Quantity, width=2,
                style={'border': '1px solid',
                       'border-color': 'lightgrey',
                       'padding-right': '0',
                       'padding-left': '0',
                       'max-width': '22%',
                       'flex': 'auto'}),
        dbc.Col(MTI_Description, width=6,
                style={'border': '1px solid',
                       'border-color': 'lightgrey',
                       'padding-right': '0',
                       'padding-left': '0',
                       'max-width': '53%',
                       'flex': 'auto'})
    ], style={'margin': '0'})

    table_body_EHS = [html.Tbody([row1EHS, row2EHS])]

    tableEHS = dbc.Table(
        table_header_EHS + table_body_EHS,
        className='table-sm text-center table-hover align-self-center')

    EHS_Input = dbc.FormGroup([
        html.H2('EHS', className="text-secondary"),
        dbc.Label("   ", html_for="Space2"),
        dbc.Label("Safety", html_for="Safety"),
        tableEHS,
        dbc.Label("EHS HighLigths:", html_for="EHS_HighLigths"),
        dbc.Textarea(id="EHS_HighLigths",
                     placeholder="Type your comments",
                     className='form-control',
                     value=ehs_highlight),
        html.Div([], style={"height": "40px"}),
    ])

    formEHS = dbc.Form([EHS_Input])
    return formEHS


# ======================================

# Main Layout==========================
app.layout = dcc.Loading(
    type='cube',
    children=[
        html.Div(
            html.Div([
                html.Div([
                    html.Div(id='dummy-input', style={'display': 'none'}),
                    html.Div([
                        html.H1('WEEKLY OPERATIONS HIGHLIGHTS' + ' -W' + Week_Number,
                                id="titleHighLights",
                                className='alert'),
                        # html.H2('MANUFACTURING', className="text-secondary"),
                    ],
                        style={
                        'position': 'relative',
                        'top': '35px',
                        'left': '7%'
                    }),
                ],
                    className="row"),
                html.Div(id='application_body', children=''),
                html.Div([
                    dbc.Button('Submit',
                               id='Submit_Button',
                               n_clicks=0,
                               style={
                                   'position': 'relative',
                                   'top': '100px',
                                   'left': '8%',
                                   'maxWidth': '100%'
                               }),
                ]),
                html.Div(id='results',
                         children='',
                         style={
                             'position': 'relative',
                             'top': '100px',
                             'left': '8%',
                             'maxWidth': '100%'
                         }),
            ], ))
    ])
# ======================================


@app.callback(Output('application_body', 'children'),
              [Input('dummy-input', 'children')])
def load_data(_):
    print("\n Initial load \n")
    username = request.authorization['username']
    print("Country Group: " + username)
    mfg_plants_data = filter_plants_by_CG(df_MFG_Plants, username)
    print(mfg_plants_data)
    print(Cal_Week)
    print(Cal_Week)
    print(username)
    mfg_mfg_data = SqlFunction.execute_query_SQL(con.QUERY_MFG_MANUFACTURING,
                                                 [Cal_Week, username])
    print("\n [Ops_Manufacturing] \n")
    print(mfg_mfg_data)
    if len(mfg_mfg_data) == 1:
        mfg_highlight = mfg_mfg_data['Highlights'][0]
        mfg_project_status = mfg_mfg_data['ProjectStatus'][0]
        mfg_support = mfg_mfg_data['Support'][0]
    else:
        mfg_highlight = ''
        mfg_project_status = ''
        mfg_support = ''

    mfg_EHS_data = SqlFunction.execute_query_SQL(con.QUERY_EHS,
                                                 [Cal_Week, username])
    print("\n [Ops_EHS] \n")
    print(mfg_EHS_data)
    if len(mfg_EHS_data) == 1:
        ehs_highlight = mfg_EHS_data['Highlights'][0]
        ehs_lti_quantity = mfg_EHS_data['LTIQuantity'][0]
        ehs_lti_description = mfg_EHS_data['LTIDescription'][0]
        ehs_mti_quantity = mfg_EHS_data['MTIQuantity'][0]
        ehs_mti_description = mfg_EHS_data['MTIDescription'][0]
    else:
        ehs_highlight = ''
        ehs_lti_quantity = 0.0
        ehs_lti_description = ''
        ehs_mti_quantity = 0.0
        ehs_mti_description = ''

    mfg_quality_data = SqlFunction.execute_query_SQL(con.QUERY_QUALITY,
                                                     [Cal_Week, username])
    print("\n [Ops_Quality] \n")
    print(mfg_quality_data)
    if len(mfg_quality_data) == 1:
        qua_heldwareinventory = mfg_quality_data['HeldwareInventory'][0]
        qua_Highlights = mfg_quality_data['Highlights'][0]
        qua_heldGenTO = mfg_quality_data['HeldwareGenTO'][0]
        qua_heldGenPercent = mfg_quality_data['HeldwareGenPercent'][0]
        qua_threeQuantity = mfg_quality_data['3Qty'][0]
        qua_fourQuantity = mfg_quality_data['4Qty'][0]
        qua_fiveQuantity = mfg_quality_data['5Qty'][0]
        qua_threeComments = mfg_quality_data['3Comments'][0]
        qua_fourComments = mfg_quality_data['4Comments'][0]
        qua_fiveComments = mfg_quality_data['5Comments'][0]

    else:
        qua_heldwareinventory = 0.0
        qua_Highlights = ''
        qua_heldGenTO = 0.0
        qua_heldGenPercent = 0.0
        qua_threeQuantity = 0.0
        qua_fourQuantity = 0.0
        qua_fiveQuantity = 0.0
        qua_threeComments = ''
        qua_fourComments = ''
        qua_fiveComments = ''

    return [
        html.Div(
            [
                dbc.Row([
                    dbc.Col(html.Div(
                        [
                            build_EHS_section(
                                ehs_highlight,
                                ehs_lti_quantity, ehs_lti_description,
                                ehs_mti_quantity, ehs_mti_description)
                        ],
                        style={
                            'width': '90%',
                            'display': 'inline-block',
                            'vertical-align': 'right'
                        }),
                        width={
                        "size": 5,
                        "order": 1
                    }),
                    dbc.Col(
                        html.Div(
                            [
                                build_quality_section(
                                    qua_heldwareinventory, qua_Highlights,
                                    qua_heldGenTO, qua_heldGenPercent,
                                    qua_threeQuantity, qua_fourQuantity,
                                    qua_fiveQuantity, qua_threeComments,
                                    qua_fourComments, qua_fiveComments)
                            ],
                            style={
                                'width': '90%',
                                'display': 'inline-block',
                                'vertical-align': 'right'
                            }),
                        width={
                            "size": 5,
                            "order": 3
                        },
                    ),
                ],
                    align="start")
            ],
            style={
                'position': 'relative',
                'top': '60px',
                'left': '8%',
                'maxWidth': '100%'
            }),
        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        html.Div([
                            build_manufacturing_section(
                                mfg_plants_data, mfg_highlight, mfg_project_status)
                        ], style={'padding-left': '0', 'padding-right': '0'}), style={'padding-left': '0', 'padding-right': '0'}),
                ],
                style={
                    'position': 'relative',
                    'top': '80px',
                    'left': '8%',
                    'right': '0',
                    'width': '80%',
                    'padding-left': '0',
                    'padding-right': '0'
                })
        ], style={'padding-left': '0', 'padding-right': '0'}),
        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        html.Div([
                            dbc.Label("   ", html_for="Space1"),
                            html.H3('Support required?',
                                    className="text-secondary"),
                            html.Div([], style={"height": "15px"}),
                            dbc.Label(
                                "Highlight any support required beyond the limits of your country group resources", html_for="Mfg_HighLights"),
                            dbc.Textarea(id="Support",
                                         style={"height": "105px"},
                                         value=mfg_support),
                        ]), ),
                ],
                style={
                    'position': 'relative',
                    'top': '80px',
                    'left': '8%',
                    'right': '0',
                    'width': '80%'
                })
        ], ),
    ]


@app.callback([
    Output('Plant1PTP', 'value'),
    Output('Plant1PTPS', 'value'),
    Output('Plant1downtime', 'value'),
    Output('Plant1mainReason', 'value')
], [Input('Plant1DD', 'value')])
def update_row_plant1(Plant1DD):
    df_plants = filter_by_plants(df_MFG_Plants, Plant1DD)
    print(df_plants)
    if len(df_plants) == 1:
        row_ptp = df_plants['PTP'][0]
        row_ptps = df_plants['PTPS'][0]
        row_downtime = df_plants['DownTime'][0]
        row_mainreason = df_plants['MainReason'][0]
    else:
        row_ptp = 0.0
        row_ptps = 0.0
        row_downtime = 0.0
        row_mainreason = ''
    return row_ptp, row_ptps, row_downtime, row_mainreason


@app.callback([
    Output('Plant2PTP', 'value'),
    Output('Plant2PTPS', 'value'),
    Output('Plant2downtime', 'value'),
    Output('Plant2mainReason', 'value')
], [Input('Plant2DD', 'value')])
def update_row_plant2(Plant2DD):
    df_plants = filter_by_plants(df_MFG_Plants, Plant2DD)
    print(df_plants)
    if len(df_plants) == 1:
        row_ptp = df_plants['PTP'][0]
        row_ptps = df_plants['PTPS'][0]
        row_downtime = df_plants['DownTime'][0]
        row_mainreason = df_plants['MainReason'][0]
    else:
        row_ptp = 0.0
        row_ptps = 0.0
        row_downtime = 0.0
        row_mainreason = ''
    return row_ptp, row_ptps, row_downtime, row_mainreason


@app.callback([
    Output('Plant3PTP', 'value'),
    Output('Plant3PTPS', 'value'),
    Output('Plant3downtime', 'value'),
    Output('Plant3mainReason', 'value')
], [Input('Plant3DD', 'value')])
def update_row_plant3(Plant3DD):
    df_plants = filter_by_plants(df_MFG_Plants, Plant3DD)
    print(df_plants)
    if len(df_plants) == 1:
        row_ptp = df_plants['PTP'][0]
        row_ptps = df_plants['PTPS'][0]
        row_downtime = df_plants['DownTime'][0]
        row_mainreason = df_plants['MainReason'][0]
    else:
        row_ptp = 0.0
        row_ptps = 0.0
        row_downtime = 0.0
        row_mainreason = ''
    return row_ptp, row_ptps, row_downtime, row_mainreason


@app.callback([
    Output('Plant4PTP', 'value'),
    Output('Plant4PTPS', 'value'),
    Output('Plant4downtime', 'value'),
    Output('Plant4mainReason', 'value')
], [Input('Plant4DD', 'value')])
def update_row_plant4(Plant4DD):
    df_plants = filter_by_plants(df_MFG_Plants, Plant4DD)
    print(df_plants)
    if len(df_plants) == 1:
        row_ptp = df_plants['PTP'][0]
        row_ptps = df_plants['PTPS'][0]
        row_downtime = df_plants['DownTime'][0]
        row_mainreason = df_plants['MainReason'][0]
    else:
        row_ptp = 0.0
        row_ptps = 0.0
        row_downtime = 0.0
        row_mainreason = ''
    return row_ptp, row_ptps, row_downtime, row_mainreason


@app.callback([
    Output('Plant5PTP', 'value'),
    Output('Plant5PTPS', 'value'),
    Output('Plant5downtime', 'value'),
    Output('Plant5mainReason', 'value')
], [Input('Plant5DD', 'value')])
def update_row_plant5(Plant5DD):
    df_plants = filter_by_plants(df_MFG_Plants, Plant5DD)
    print(df_plants)
    if len(df_plants) == 1:
        row_ptp = df_plants['PTP'][0]
        row_ptps = df_plants['PTPS'][0]
        row_downtime = df_plants['DownTime'][0]
        row_mainreason = df_plants['MainReason'][0]
    else:
        row_ptp = 0.0
        row_ptps = 0.0
        row_downtime = 0.0
        row_mainreason = ''
    return row_ptp, row_ptps, row_downtime, row_mainreason


@app.callback(Output("results", "children"),
              [Input('Submit_Button', 'n_clicks')], [
                  State('Plant1DD', 'value'),
                  State('Plant1PTP', 'value'),
                  State('Plant1PTPS', 'value'),
                  State('Plant1downtime', 'value'),
                  State('Plant1mainReason', 'value'),
                  State('Plant2DD', 'value'),
                  State('Plant2PTP', 'value'),
                  State('Plant2PTPS', 'value'),
                  State('Plant2downtime', 'value'),
                  State('Plant2mainReason', 'value'),
                  State('Plant3DD', 'value'),
                  State('Plant3PTP', 'value'),
                  State('Plant3PTPS', 'value'),
                  State('Plant3downtime', 'value'),
                  State('Plant3mainReason', 'value'),
                  State('Plant4DD', 'value'),
                  State('Plant4PTP', 'value'),
                  State('Plant4PTPS', 'value'),
                  State('Plant4downtime', 'value'),
                  State('Plant4mainReason', 'value'),
                  State('Plant5DD', 'value'),
                  State('Plant5PTP', 'value'),
                  State('Plant5PTPS', 'value'),
                  State('Plant5downtime', 'value'),
                  State('Plant5mainReason', 'value'),
                  State('Mfg_HightLights', 'value'),
                  State('Support', 'value'),
                  State('HeldW_GenTO', 'value'),
                  State('HeldW_Gen_Percent', 'value'),
                  State('Inventory_TO', 'value'),
                  State('Quantity_complaints5', 'value'),
                  State('Quantity_complaints4', 'value'),
                  State('Quantity_complaints3', 'value'),
                  State('Comment_complaints5', 'value'),
                  State('Comment_complaints4', 'value'),
                  State('Comment_complaints3', 'value'),
                  State('Qua_Highligths', 'value'),
                  State('LTI_Quantity', 'value'),
                  State('LTI_Description', 'value'),
                  State('MTI_Quantity', 'value'),
                  State('MTI_Description', 'value'),
                  State('EHS_HighLigths', 'value'),
                  State('Project_Status', 'value'),
])
def save_highLights(
        n1, Plant1DD, Plant1PTP, Plant1PTPS, Plant1downtime, Plant1mainReason,
        Plant2DD, Plant2PTP, Plant2PTPS, Plant2downtime, Plant2mainReason,
        Plant3DD, Plant3PTP, Plant3PTPS, Plant3downtime, Plant3mainReason,
        Plant4DD, Plant4PTP, Plant4PTPS, Plant4downtime, Plant4mainReason,
        Plant5DD, Plant5PTP, Plant5PTPS, Plant5downtime, Plant5mainReason,
        Mfg_HightLights, Support, HeldW_GenTO, HeldW_Gen_Percent, Inventory_TO,
        Quantity_complaints5, Quantity_complaints4, Quantity_complaints3,
        Comment_complaints5, Comment_complaints4, Comment_complaints3, Qua_Highligths,
        LTI_Quantity, LTI_Description, MTI_Quantity, MTI_Description,
        EHS_HighLigths, Project_Status):
    if n1 == 0 or not n1:
        pass
    else:
        try:
            country_group = request.authorization['username']
            print("Trying to save the data")

            quality_records = insert_update_quality(
                Cal_Week, country_group, Inventory_TO, Qua_Highligths,
                HeldW_GenTO, HeldW_Gen_Percent,
                Quantity_complaints3, Quantity_complaints4,
                Quantity_complaints5, Comment_complaints3,
                Comment_complaints4, Comment_complaints5)

            ehs_records = insert_update_ehs(Cal_Week, country_group,
                                            LTI_Quantity, MTI_Quantity,
                                            LTI_Description, MTI_Description,
                                            EHS_HighLigths)

            manufacturing_records = insert_update_manufacturing(
                Cal_Week, country_group, Mfg_HightLights, Project_Status,
                Support)

            if Plant1DD != '' and Plant1DD is not None:
                plant1_records = insert_update_mfg_plants(
                    Cal_Week, country_group, Plant1DD, Plant1PTP, Plant1PTPS,
                    Plant1mainReason, Plant1downtime)
            else:
                plant1_records = None

            if Plant2DD != '' and Plant2DD is not None:
                plant2_records = insert_update_mfg_plants(
                    Cal_Week, country_group, Plant2DD, Plant2PTP, Plant2PTPS,
                    Plant2mainReason, Plant2downtime)
            else:
                plant2_records = None

            if Plant3DD != '' and Plant3DD is not None:
                plant3_records = insert_update_mfg_plants(
                    Cal_Week, country_group, Plant3DD, Plant3PTP, Plant3PTPS,
                    Plant3mainReason, Plant3downtime)
            else:
                plant3_records = None

            if Plant4DD != '' and Plant4DD is not None:
                plant4_records = insert_update_mfg_plants(
                    Cal_Week, country_group, Plant4DD, Plant4PTP, Plant4PTPS,
                    Plant4mainReason, Plant4downtime)
            else:
                plant4_records = None

            if Plant5DD != '' and Plant5DD is not None:
                plant5_records = insert_update_mfg_plants(
                    Cal_Week, country_group, Plant1DD, Plant5PTP, Plant5PTPS,
                    Plant5mainReason, Plant5downtime)
            else:
                plant5_records = None

            if 0 in {
                    quality_records, ehs_records, manufacturing_records,
                    plant1_records, plant2_records, plant3_records,
                    plant4_records, plant5_records
            }:
                return 'An error ocurred saving your data, some of it might not have saved.'
            else:
                return 'Data saved succesfully'
        except:
            print("Algo salió mal\n")
            traceback.print_stack()
            return 'An unexpected error occurred, your data might not be saved'


if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0',debug=False,dev_tools_ui=False,dev_tools_props_check=False)

