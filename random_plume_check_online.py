#==============================================================================
## Plot and trim population count 
#==============================================================================
# Uses modules:
import pandas as pd
import numpy as np
import random
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
import random
from glob import glob
import base64
import os
import dash_bootstrap_components as dbc
from datetime import datetime as dt
#==============================================================================


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
##external_stylesheets=[dbc.themes.SPACELAB]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


##data[0]['State'] = dcc.Markdown('''![alt text]({} "Logo Title Text 1")
##    '''.format(app.get_asset_url('Plume_images/' + image_filename)))

##df['State'].loc[0] = dcc.Markdown('''
##    ![alt text]({} "Logo Title Text 1")
##    '''.format(app.get_asset_url('Plume_images/' + image_filename)))

app.layout = html.Div([
    dcc.Store(id='memory'),
    html.H1('Pollution Plume Finder', style={'textAlign': 'center'}),
##    dcc.Markdown('''![plume_image](https://s0.geograph.org.uk/geophotos/03/22/03/3220320_1df4aa5c.jpg)'''),
    html.Br(),
    html.P('Info info info'),
    html.Hr(),
    html.H3('What is a plume?'),
    html.P('Explanation and examples'),
    html.Hr(),
    html.H3('Instructions'),
    html.P('What to do....'),
    html.Hr(),
    html.Button('Load New Images',id = 'load_images'),
    html.P('(Pressing this will lose any images selected but not saved)'),

    html.Div(id = 'Tableholder'),
    dash_table.DataTable(
            id='table',
        ##    columns=[{"name": i, "id": i} for i in df.columns],
            columns = [dict(name='a', id='a', type='text', presentation='markdown'),
                       dict(name='b', id='b', type='text', presentation='markdown'),
                       dict(name='c', id='c', type='text', presentation='markdown'),
                       dict(name='d', id='d', type='text', presentation='markdown'),
                       dict(name='e', id='e', type='text', presentation='markdown'),
                       dict(name='f', id='f', type='text', presentation='markdown'),
                       ],
            style_table={
##            'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
            'minWidth': '900px', 'width': '900px', 'maxWidth': '900px'},
            style_header = {'display': 'none'},
            style_cell = {'padding':'5px'},
            style_data_conditional=[]
                        ),
    html.Div(id = 'selected_cells', style= {'display':'none'}),
    html.Br(),
    
    html.P('Click the button below to submit your selection. Any image not selected will be labelled as no plume'),
    html.Button('Submit Selection',id = 'selection_save'),
    html.Hr(),
        
])

@app.callback([Output('table', 'data'),
               Output('memory','clear_data'),
               Output('table','active_cell')],
              [Input('load_images', 'n_clicks')])
def render_table_content(n_clicks):
    
    images = glob('/Users/dfinch/Python/Plume_Detection/assets/Plume_images/*')

    random_images = random.choices(images,k = 18)
    image_filenames = [fn.split('/')[-1] for fn in random_images]

    data=[]
    f_num = 0
    for row in range(3):
        row_dict = {}
        for letter in ['a','b','c','d','e','f']:
            row_dict[letter] = '''![plume_image]({})'''.format(app.get_asset_url('Plume_images/' + image_filenames[f_num]))
            f_num += 1
        data.append(row_dict)
    
    return data,True, None

@app.callback([Output('table', 'style_data_conditional'),
               Output('memory','data')],
              [Input('table', 'active_cell')],
              [State('memory','data')])
def cell_clicked(active_cell,mem_data):
    if mem_data:
        condition = mem_data
    else:
        condition = [{'if':{'state':'selected'},'backgroundColor':'#FF4136'}]
        
    if active_cell:
        cond_command =  {'if':{'column_id':active_cell['column_id'], 'row_index':active_cell['row']},'backgroundColor':'#FF4136'}
        if {'if':{'state':'selected'},'backgroundColor':None} in condition:
            condition.remove({'if':{'state':'selected'},'backgroundColor':None})
            condition.append({'if':{'state':'selected'},'backgroundColor':'#FF4136'})
            
        if cond_command in condition:
            condition.remove(cond_command)
            condition.append({'if':{'state':'selected'},'backgroundColor':None})
        else:
            condition.append(cond_command)
        return condition, condition
        
    else:
        return [{'if':{'state':'selected'},'backgroundColor':None}], []

@app.callback(Output('load_images', 'n_clicks'),
              [Input('selection_save', 'n_clicks')],
              [State('memory','data'),
               State('table','data')])
def save_selection(n_clicks,mem_data,table_data):
    print(table_data)
    conds = []
    if n_clicks:
        plume_df = pd.DataFrame(columns = ['Plume'])
        for row in table_data:
            for col in row.keys():
                raw_string = row[col]
                image_num = (raw_string.split('_')[-1].split('.png')[0])
                plume_df.loc[image_num] = False
        if mem_data:
            for c in mem_data:
                if c['if'] == {'state': 'selected'}:
                    continue
                conds.append(c['if'])

            coords_df = pd.DataFrame.from_dict(conds)
            for ind,row in coords_df.iterrows():
                raw_string = table_data[row.row_index][row.column_id]
                image_num = (raw_string.split('_')[-1].split('.png')[0])
                plume_df.loc[image_num] = True
            
        plume_df.to_csv('{}/PlumeOutput/{}.csv'.format(os.getcwd(),dt.timestamp(dt.now())))
        return n_clicks
    else:
        return None
if __name__ == '__main__':
    app.run_server(debug=True)
