from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import dirname, join
import pandas as pd

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

pcDat = pd.DataFrame.from_csv(join(dirname(__file__), 'pcaLoadingsForImputedSireGenomes.txt'), sep='\t')
#pcDat = pd.DataFrame.from_csv(join('C:\Users\matthew.weiser\Dropbox (Plusvital Limited)\RESEARCH FOLDER\MCW\stalloinRelatedness_demoApp\\app', 'pcaLoadingsForImputedSireGenomes.txt'), sep='\t')
#pcDat["PC1"]
pcDat = pcDat[["PC1","PC2","PC3","PC4","PC5","PC6"]]
pcDat["color"] = "grey"
pcDat["alpha"] = 0.3
refHorses = pcDat.index

from app import models

