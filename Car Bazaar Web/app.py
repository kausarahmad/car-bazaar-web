import pickle
import numpy as np
import re
import datetime
from flask import Flask, render_template, request

import sys
sys.path.insert(1, sys.path[0]+'\\util')
from transformations import transform_badge
from util_database import *

from google_images_search import GoogleImagesSearch
import os
import glob

def fetch_img(query):

    files = glob.glob(sys.path[0]+'\\static\\img\\chat page car\\*')
    for f in files:
        os.remove(f)

    gis = GoogleImagesSearch('AIzaSyCR0DCaMCyhKNU8Sxnlg9d5gDoRfGqlF4E', '016040578520524185149:aj1ixvinhes')

    _search_params = {
        'q': query,
        'num': 10,
        'fileType': 'jpg'
    }

    gis.search(search_params=_search_params)
    for image in gis.results():
        image.download(sys.path[0]+"\\static\\img\\chat page car")

    fnames = os.listdir(sys.path[0]+'\\static\\img\\chat page car\\')
    if len(fnames)>=1:
        return fnames[0]
    else:
        _search_params = {
        'q': query,
        'num': 20,
        'fileType': 'jpg'
        }

        gis.search(search_params=_search_params)
        for image in gis.results():
            image.download(sys.path[0]+"\\static\\img\\chat page car")

        fnames = os.listdir(sys.path[0]+'\\static\\img\\chat page car\\')
        return fnames[0]

def predict(make,model,fuel,body,year,km,badgeo,city):
    error = 100

    now = datetime.datetime.now()
    datetime_year = int(now.strftime("%Y"))
    datetime_month = int(now.strftime("%m"))
    badge = transform_badge(badgeo)
    make = get_make(make)
    model = get_model(model)
    fuel = get_fuel(fuel)
    body = get_body(body)
    
    #LOAD MODEL
    pkl_file_badge = open('models/LE01-badge_transformed.pkl', 'rb')
    le_badge_transformed = pickle.load(pkl_file_badge) 
    pkl_file_badge.close()

    pkl_file_coordinates = open('models/LE01-coordinates2city.pkl', 'rb')
    le_coordinates2city = pickle.load(pkl_file_coordinates) 
    pkl_file_coordinates.close()
    
    filename = 'models/M01-RandomForestRegressor.sav'
    regressor = pickle.load(open(filename, 'rb'))
    
    #PREDICT
    badge = int(le_badge_transformed.transform([badge])[0])
    city = int(le_coordinates2city.transform([city])[0])
    pred = regressor.predict(np.array([make, model, fuel, body, year, km, badge, city, datetime_year, datetime_month]).reshape(1,-1))
    pred1 = round(pred[0]-error)
    pred2 = round(pred[0]+error)
    return str(pred1)+" - "+str(pred2)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        make = request.form['make'].capitalize()
        model = request.form['model'].capitalize()
        badge = request.form['badge'].capitalize()
        fuel = request.form['fuel'].capitalize()
        body = request.form['body'].capitalize()
        km = request.form['km']
        year = request.form['year']
        city = request.form['city'].capitalize()

        imgfilename = fetch_img(make+" "+model+" "+badge+" "+year+" "+body+" "+fuel)

        price = predict(make,model,fuel,body,year,km,badge,city)

        return render_template('chat.html', imgcar = "img/chat page car/" + imgfilename, price = price, make = make, model = model, 
            badge = badge, fuel = fuel, body = body, km = km, year = year, city = city)
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
