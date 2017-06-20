from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import dirname, join
import pandas as pd
import ast
import os

import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc
from bokeh.embed import components 

from app import app, models
    
db = SQLAlchemy(app)

#pcDat = pd.DataFrame.from_csv(join('C:\Users\matthew.weiser\Dropbox (Plusvital Limited)\RESEARCH FOLDER\MCW\stalloinRelatedness_demoApp\\app', '\\app\pcaLoadingsForImputedSireGenomes.txt'), sep='\t')
print os.path.dirname(os.path.abspath(__file__))  
pcDat = pd.DataFrame.from_csv(join(os.path.dirname(os.path.abspath(__file__)), 'app\pcaLoadingsForImputedSireGenomes.txt'), sep='\t')
#pcDat["PC1"]
pcDat = pcDat[["PC1","PC2","PC3","PC4","PC5","PC6"]]
pcDat["color"] = "grey"
pcDat["color"] = "grey"
pcDat["alpha"] = 0.3
refHorses = pcDat.index.values.tolist() 


u = models.User.query.filter_by(uname='testuser')
if u.count() == 1:
    horsenames = [h.hname for h in u.first().horses ]  
    horseids = [h.id for h in u.first().horses ]      
    user = {'customer_name': u.first().uname, 'horsenames': horsenames, 'horseids': horseids}

# compile all the horse info into the pcDat table:
pcDat_full = pcDat
for i in user['horseids']:
    tmp = models.Horse.query.filter_by(id=i)
    dftmp = pd.DataFrame({"PC1": tmp.first().pc1,
    "PC2": tmp.first().pc2,
    "PC3": tmp.first().pc3,
    "PC4": tmp.first().pc4,
    "PC5": tmp.first().pc5,
    "PC6": tmp.first().pc6,
    "color": "orange",
    "alpha": 0.9}, index=[tmp.first().hname] )
    pcDat_full = pd.concat([pcDat_full,dftmp])

# read in the data frame with the pre-loaded PCs:
axis_map = {
  "PC1 (Danehill bloodline)": "PC1",
  "PC2 (Sadler's Wells bloodline)": "PC2",
  "PC3 (Green Desert bloodline)": "PC3",
  "PC4 (Zabeel bloodline)": "PC4",
  "PC5 (A.P. Indy bloodline)": "PC5"    
}

desc = Div(text=open(join(os.path.dirname(os.path.abspath(__file__)), 'app\\templates', "description.html")).read(), width=800)

horseList = Select(title="Horses", value="All",
                   options=['All'] + user['horsenames'])
# Create Input controls
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="PC1 (Danehill bloodline)")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="PC2 (Sadler's Wells bloodline)") 
# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], name=[],  alpha=[]))    
hover = HoverTool(tooltips=[
  ("Name", "@name")#,
  #("Similarity Score", "@genomeSimScore")
  ])    
p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tools=[hover])
p.circle(x="x", y="y", source=source, size=7, color="color", line_color=None, fill_alpha="alpha")

def select_horses():
    horse_val = horseList.value
    if horse_val == 'All':
        horses_to_plot = pcDat_full.index
    else:
        horses_to_plot = refHorses + [horse_val]        
    selected = pcDat_full.ix[ horses_to_plot ]     
    return [selected, len(refHorses), len(horses_to_plot)-len(refHorses)]

def update():
    tmp = select_horses()
    df =tmp[0]
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d horses selected : %d stallions, %d customer-horse(s)" % (len(df), tmp[1], tmp[2])
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        color=df["color"],
        name=df.index,
        #year=df["Year"],
        #revenue=df["revenue"],
        alpha=df["alpha"]
        )
#script, div = components(p)          
#return render_template('index.html', 
#title='Genome Explorer Home Page', user=user, div=div, script=script)

controls = [ x_axis, y_axis, horseList]
for control in controls:
  control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
  [desc],
  [inputs, p],
  ], sizing_mode=sizing_mode)

update()  # initial load of the data
curdoc().add_root(l)
curdoc().title = "Harses"


#script, div = components(p)          
#return render_template('index.html', 
#title='Genome Explorer Home Page', user=user, div=div, script=script)



