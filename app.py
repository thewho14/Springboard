# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
rfc = joblib.load('model.pkl')

app = dash.Dash()


#app.css.append_css({
#    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css"
#})

app.layout = html.Div(children=[
    html.H1(children='Affordability Predictor'),

    html.Div(children='''
        Answer 20 questions to find out how affordable your new unit will be.
    '''),
     html.Br(),        
     html.Label('Where is the unit located?  '),
     dcc.Dropdown(id = 'city',
            options=[
                    {'label':'New York City','value': 5600},
                    {'label':'Los Angeles', 'value': 4480},
                    {'label':'Detroit', 'value': 2160},
                    {'label':'Philadelphia','value': 6160},
                    {'label':'Chicago','value': 1600},
                    {'label':'Washington D.C.', 'value':8840},
                    {'label':'Houston', 'value':3360},
                    {'label':'San Diego', 'value':7320},
                    {'label':'Anaheim', 'value':0360},
                    {'label':'Boston', 'value':1120},
                    {'label':'Dallas', 'value':1920},
                    {'label':'Oakland', 'value':5775},
                    {'label':'Phoenix', 'value':6200},
                    {'label':'Minneapolis-Saint Paul', 'value':5120},
                    {'label':'Seattle', 'value':7600}
                    ],
                    placeholder = 'Please Select a City',
                    ),
     html.Br(),
     html.Label('Does the unit have a working fireplace?'),
     dcc.RadioItems(id = 'Fire',
                    options=[
                            {'label':'Yes','value':1},
                            {'label':'No','value':2}
                            ],
             value = 1),
     html.Br(),
     html.Label('Does the unit have a working dishwasher?'),
     dcc.RadioItems(id = 'Dish',
                    options=[
                            {'label':'Yes','value':1},
                            {'label':'No','value':2}
                            ],
             value = 1),
     html.Br(),
     html.Label('Does the unit have a Garage or Carport?'),
     dcc.RadioItems(id = 'Car',
                    options=[
                            {'label':'Yes','value':1},
                            {'label':'No','value':2}
                            ],
             value = 1),
     html.Br(),
     html.Label('Is the unit Handicap Accessible?'),
     dcc.RadioItems(id = 'Handi',
                    options=[
                            {'label':'Yes','value':1},
                            {'label':'No','value':2}
                            ],
             value = 1),
     html.Label('Does the unit have a working garbage disposal?'),
     dcc.RadioItems(id = 'Disp',
                    options=[
                            {'label':'Yes','value':1},
                            {'label':'No','value':2}
                            ],
             value = 1),
     html.Br(),
     html.Label('If there is no garage, is a driveway/lot/parking area off the street provided?'),
     dcc.RadioItems(id = 'Park',
                    options=[
                            {'label':'Yes','value':1},
                            {'label':'No','value':2},
                            {'label':'Unit has a Garage','value':-6}
                            ],
             value = 1),
     html.Br(),
     html.Label('How many square feet is the unit?'),
     dcc.Input(id = 'sf', value = '',type = 'number'),
     html.Br(),
     html.Br(),
     html.Label('How many square feet is the lot the unit sits on?'),
     dcc.Input(id = 'lotsf', value = '',type = 'number'),
     html.Br(),
     html.Br(),
     html.Label('What year was the unit built?'),
     dcc.Input(id = 'year', value = '',type = 'number'),
     html.Br(),
     html.Br(),
     html.Label('How many floors in the unit?'),
     dcc.Input(id = 'floors', value='',type='number'),
     html.Br(),
     html.Br(),
     html.Label('How many full bathrooms does the unit have?'),
     dcc.Input(id = 'baths', value='',type='number'),
     html.Br(),
     html.Br(),
     html.Label('How many laundry, utility, and pantry rooms in the unit?'),
     dcc.Input(id = 'laundry', value='',type='number'),
     html.Br(),
     html.Br(),
     html.Label('How many individual housing units in the building?'),
     dcc.Input(id = 'nunits', value='',type='number'),
     html.Br(),
     html.Br(),
     html.Label('How many floors from the building entrance to the unit?'),
     dcc.Input(id = 'climb', value='',type='number'),
     html.Br(),
     html.Br(),
     html.Label('How many dining rooms in the unit?'),
     dcc.Input(id = 'dining', value='',type='number'),
     html.Br(),
     html.Br(),
     html.Label('Rate the safety of the neighborhood surrounding the unit.'),
     dcc.Dropdown(id = 'safe',
             options = [
                     {'label':'Very Safe','value':1},
                     {'label':'Somewhat Safe','value':2},
                     {'label':'Somewhat Dangerous','value':3},
                     {'label':'Very Dangerous','value':4}
                     ],
                     value = 1),
     html.Br(),
     html.Label('What is underneath the building?'),
     dcc.Dropdown(id = 'basement',
             options = [
                     {'label':'Basement under the whole building','value':1},
                     {'label':'Basement under part of the building','value':2},
                     {'label':'Crawl space','value':3},
                     {'label':'Concrete slab','value':4}
                     ],
             value = 1),
     html.Br(),
     html.Label('How is the unit heated?'),
     dcc.Dropdown(id = 'heat',
             options = [
                     {'label':'Forced warm air furnace w/ duct and vent to individual rooms','value':1},
                     {'label':'Radiators or other system using steam or hot water','value':2},
                     {'label':'Electric heat pump','value':3},
                     {'label':'Built-in electric baseboard heating or electric coils in floors, ceilings, or walls','value':4},
                     {'label':'Floor, wall, or other pipeless furnace built into the building','value':5}
                     ],
                     value=1),
     html.Br(),
     html.Label('How is water heated in this unit?'),
     dcc.Dropdown(id = 'water',
             options = [
                     {'label':'Electricity','value':1},
                     {'label':'Gas (including liquid propane','value':2},
                     {'label':'Fuel Oil','value':3},
                     {'label':'Kerosene or other liquid fuel','value':4},
                     {'label':'Coal or coke','value':5},
                     {'label':'Wood','value':6},
                     {'label':'Solar energy','value':7}
                     ], value = 1
             ),
      html.Br(),
      html.H2(id='out'),
     
     ], style={'columnCount': 2})
@app.callback(
    dash.dependencies.Output('out', 'children'),
    [dash.dependencies.Input('city', 'value'),
     dash.dependencies.Input('Fire', 'value'),
     dash.dependencies.Input('Dish', 'value'),
     dash.dependencies.Input('Car', 'value'),
     dash.dependencies.Input('Handi', 'value'),
     dash.dependencies.Input('Disp', 'value'),
     dash.dependencies.Input('Park', 'value'),
     dash.dependencies.Input('sf', 'value'),
     dash.dependencies.Input('lotsf', 'value'),
     dash.dependencies.Input('year', 'value'),
     dash.dependencies.Input('floors', 'value'),
     dash.dependencies.Input('baths', 'value'),
     dash.dependencies.Input('laundry', 'value'),
     dash.dependencies.Input('nunits', 'value'),
     dash.dependencies.Input('climb', 'value'),
     dash.dependencies.Input('dining', 'value'),
     dash.dependencies.Input('safe', 'value'),
     dash.dependencies.Input('basement','value'),
     dash.dependencies.Input('heat','value'),
     dash.dependencies.Input('water','value')])

def update_output_div(i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20):
    sample = np.array([i1,i10,i8,i12,i9,i2,i11,i3,i18,i14,i19,i16,i20,i17,i7,i6,i15,i4,i5,i13])
    pred = rfc.predict(sample)
    if i1 == 5600:
        k = 'New York City'
    elif i1 == 4480:
        k = 'Los Angeles'
    elif i1 == 2160:
        k = 'Detroit'
    elif i1 == 6160:
        k = 'Philadelphia'
    elif i1 == 1600:
        k = 'Chicago'
    elif i1 == 8840:
        k = 'Washington D.C.'
    elif i1 == 3360:
        k = 'Houston'
    elif i1 == 7320:
        k = 'San Diego'
    elif i1 == 0360:
        k = 'Anaheim'
    elif i1 == 1120:
        k = 'Boston'
    elif i1 == 1920:
        k = 'Dallas'
    elif i1 == 5775:
        k = 'Oakland'
    elif i1 == 6200:
        k = 'Phoenix'
    elif i1 == 5120:
        k = 'Minneapolis-Saint Paul'
    elif i1 == 7600:
        k = 'Seattle'
    if pred == 0:
        return 'This unit is NOT AFFORDABLE for the average inhabitant of {}'.format(k)
    elif pred == 1:
        return 'This unit IS AFFORDABLE for the average inhabitant of {}'.format(k)
    else:
        return 'Opps something went wrong!'
    
if __name__ == '__main__':
  app.run_server(debug=True)
    
