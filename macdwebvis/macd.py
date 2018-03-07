import pandas as pd

import os
import json
import datetime
import random
import time
from flask import Flask, request, render_template
#from bson.json_util import dumps, default

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publish')
def publish():
	cat = request.args.get("Category")
	cat = cat.replace('AND','&')

	df = data
	nut = pd.concat([df['Total Fat'], df["Cholesterol"], df["Sodium"], df["Carbohydrates"], df["Sugars"], df["Protein"],df["Vitamin A (% Daily Value)"]]
,axis=1)
	zscore = lambda x: (x - x.mean()) / x.std()
	nut = nut.transform(zscore)+2

	df = pd.concat([df["Category"],df["Item"],df["Calories"],nut],axis=1)
	group = df.groupby("Category").get_group(cat)
	group = group.drop("Category",axis=1).to_json(orient='records')
#df["Vitamin A (% Daily Value)"], df["Vitamin C (% Daily Value)"
	return group#json.dumps(group)

if __name__ == "__main__":
	data = pd.read_csv("./static/menu.csv")
	data = data.drop("Total Fat (% Daily Value)", axis = 1)
	data = data.drop("Saturated Fat (% Daily Value)", axis = 1)
	data = data.drop("Cholesterol (% Daily Value)", axis = 1)
	data = data.drop("Carbohydrates (% Daily Value)", axis = 1)
	data = data.drop("Dietary Fiber (% Daily Value)", axis = 1)
	data = data.drop("Sodium (% Daily Value)", axis = 1)
	corr_matrix = data.iloc[:,3:].corr(method='pearson')
	corr_matrix.to_csv("./static/menu_corr.csv")

	df = pd.read_csv("./static/menu.csv")
	df_main = pd.concat([df["Category"],df["Calories"],df['Total Fat'], df["Cholesterol"], df["Sodium"], df["Carbohydrates"], df["Sugars"], df["Protein"], df["Vitamin A (% Daily Value)"],],axis=1)
	by_category = df_main.groupby("Category")
	zscore = lambda x: (x - x.mean()) / x.std()
	mean = by_category.mean()
	mean_norm = mean.transform(zscore) + 2
	mean_norm.to_csv("./static/menu_mean.csv")

	app.run(debug=True)