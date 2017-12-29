# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:08:11 2017

@author: zhutk
"""

'''psedu code for the app

First take in preferences.  Users are asked at the top of the page to rate the beer groups from 1-5.
Users start with a rating of 3 for every beer by default so that a user is not required to select preferences
in order to the recommendation list.  The default vector of three is modified by ratings input by the user.
The ratings are then used to boost or lower beer rating in the dataset.  Later the recommendation algorithm
will be called in order to predict beer scores for the beer list and the scores will be used to order the beer list.
(Preferably this feature would live update rapidly creating the modified dataset and then feed through the whole process
but if the update process takes too long it makes more sense to have an update button to lock in preferences instead.)

import modules

1. Preferences
print 'Rate the following beer groups on a 1-5 scale'

take rating input and create preference vector

use preference vector to modify dataset

2. Creating Beer List
print 'Search for beers, breweries, or both'

Search entry feeds in Whoosh and returns the top 20 hits

Radio buttons to select which option in search results you meant

2a. Search by custom beer list
Add button to add the selected option to the list (looks up the selected beer in the dataset in order to also add beer_id)

2b. Search by brewery
Once brewery is selected, the name is looked up in the dataset and all beers with matching brewery name are used to
create beer list.

3. Sort beer list (this section should live update so that beers are sorted as they are added to the list)
The recommendation algorithm is trained on the modified dataset from step one.

Recommendation algorithm used to predict rating for all beers in the beer list

Beer list is sorted by predicted ratings

Return beer list to user'''
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from whoosh.qparser import QueryParser, MultifieldParser

df = pd.read_csv('Beer_Dataset',encoding='utf-8')

from whoosh.index import open_dir

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer

'''schema = Schema(beer_id=STORED(),
                brewery=TEXT(stored=True),
                beer=TEXT(stored=True),
                group=KEYWORD)'''

ix = open_dir("index")

app = dash.Dash()

#app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css"})
app.css.append_css({'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'})

rscale = ['','Hate', 'Dislike','Neutral','Like', 'Love']

app.layout = html.Div(children=[
        html.H1(children='Beer Maven'),
        html.Label('Please rate the following beer groups on a 1-5 scale'),
        html.Div(),
        html.Br(),
        html.Label('IPAs and Pale Ales'),
        #html.Br(),
        dcc.Slider(min=1, max=5, step=1,value=3, marks=rscale, id = 'IPA'),
        html.Br(),
        html.Br(),
        html.Label('Dark Ales'),
        #html.Br(),
        dcc.Slider(min=1, max=5, step=1,value=3, marks=rscale, id = 'DA'),
        html.Br(),
        html.Br(),
        html.Label('Porter and Stouts'),
        #html.Br(),
        dcc.Slider(min=1, max=5, step=1,value=3, marks=rscale, id = 'PS'),
        html.Br(),
        html.Br(),
        html.Label('Pale Lagers'),
        #html.Br(),
        dcc.Slider(min=1, max=5, step=1,value=3, marks=rscale, id = 'PL'),
        html.Br(),
        html.Br(),
        html.Label('Dark Lagers'),
        #html.Br(),
        dcc.Slider(min=1, max=5, step=1,value=3, marks=rscale, id = 'DL'),
        html.Br(),
        html.Br(),
        html.Label('Wheat Beers'),
        #html.Br(),
        dcc.Slider(min= 1, max=5, step=1,value=3, marks=rscale, id = 'WB'),
        html.Br(),
        html.Br(),
        html.Label('High ABV'),
        #html.Br(),
        dcc.Slider(min=1, max=5, step=1,value=3, marks=rscale, id = 'HA'),
        html.Br(),
        html.Br(),
        html.Label('Spiced/Fruity Beers'),
        #html.Br(),
        dcc.Slider(min=1, max=5, step=1,value=3, marks=rscale, id = 'SF'),
        html.Br(),
        html.Br(),
        html.Label('Non-Alcoholic'),
        dcc.Slider(min=1, max=5, step=1,value=3, marks = rscale, id = 'NA'),
        html.Br(),
        html.Button(id='Button',n_clicks=0,children = 'Apply'),
        html.Div(id='out1', style={'display': 'none'}),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Label('Search for Brewery and/or Beer'),
        dcc.Input(id = 'search', value=''),
        html.Button(id = 'search button',n_clicks = 0, children = 'Search'),
        html.H2(id='out2')
        ])
@app.callback(
    Output(component_id='out1', component_property='children'),
    [Input(component_id = 'Button',component_property='n_clicks')],
    [State(component_id='IPA', component_property='value'),
     State(component_id='DA', component_property='value'),
     State(component_id='PS', component_property='value'),
     State(component_id='PL', component_property='value'),
     State(component_id='DL', component_property='value'),
     State(component_id='WB', component_property='value'),
     State(component_id='HA', component_property='value'),
     State(component_id='SF', component_property='value'),
     State(component_id='NA', component_property='value')]
)
def add_pref(n,IPA, DA, PS, PL, DL, WB, HA, SF, NA):
    #return '{} You\'ve entered "{}"'.format(n,[IPA,DA,PS,PL,DL,WB,HA,SF])
    pref_vect = [IPA,DA,PS,PL,DL,WB,HA,SF,NA]
    data = df.copy()
    grouped = data.group.value_counts().index.values
    for x in range(len(grouped)-1):
        score = data[data.group==grouped[x]].rating
        if pref_vect[x] == 1:
            data.loc[data.group==grouped[x],'rating'] = score - .5
        if pref_vect[x] == 2:
            data.loc[data.group==grouped[x],'rating'] = score - .25
        if pref_vect[x] == 4:
            data.loc[data.group==grouped[x],'rating'] = score + .25
        if pref_vect[x] == 5:
            data.loc[data.group==grouped[x],'rating'] = score + .5
        data.loc[data.rating > 5,'rating'] = 5
    return data.to_json()

@app.callback(
        Output(component_id='out2', component_property='children'),
        [Input(component_id='search button', component_property='n_clicks')],
        [State(component_id='search', component_property= 'value')]
        )

def search_df(n, entry):
    try:
        qp = MultifieldParser(["brewery","beer"], schema=ix.schema)
        q = qp.parse(unicode(entry))
        #q = qp.parse('ballast point sculpin IPA')
        with ix.searcher() as s:
            results = s.search(q)
            a = results[0]['beer']
            b = results[0]['brewery']
            c = results[0]['beer_id']
            d = results[1]['beer']
            e = results[1]['brewery']
            f = results[1]['beer_id']
            g = results[2]['beer']
            h = results[2]['brewery']
            i = results[2]['beer_id']
            
            #for line in
            return 'Result 1: Beer: {} Brewery: {}  ID: {}'.format(a,b,c) + 'Result 2: Beer: {}  Brewery: {} ID: {}'.format(d,e,f) + 'Result 3: Beer: {} Brewery: {} ID: {}'.format(g,h,i)
            #return 
        #find way to make output results dropdown or radio buttons
    except:
        return '{}'.format(type(unicode(entry)))
        #return '{}, {}'.format(results[0]['brewery'],results[0]['beer'])

if __name__ == '__main__':
    app.run_server(debug=True)