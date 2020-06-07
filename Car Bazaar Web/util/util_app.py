import re
import numpy
import pickle
import sys
import datetime

from google_images_search import GoogleImagesSearch
import os
import glob

from util_database import *

def transform_badge(badge):
    try:
        if (numpy.isnan(badge)):
            badge = ''
            return badge
    except:
        pass
    badge = re.sub(r"(?i)(^no$)|(^all\W?others$)", "", badge)
    badge = re.sub(r"^[^0-9A-Za-z]+$", "", badge)
    badge = badge.upper()
    badge = re.sub(r"-| ", "", badge)
    badge = re.sub(r"(?i)4WD", "4X4", badge)
    badge = re.sub(r"(?i)lpg", "", badge)
    
    return badge

def save_dict(make, model, fuel, body, year, km, badge, city):

    car_dict = {}
    car_dict['make'] = make
    car_dict['model'] = model
    car_dict['fuel_type'] = fuel
    car_dict['body_type'] = body
    car_dict['year'] = year
    car_dict['km'] = km
    car_dict['badge'] = badge
    car_dict['city'] = city

    return car_dict


def fetch_img(query):

    #remove existing images
    files = glob.glob('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\chat page car\\*')
    for f in files:
        os.remove(f)

    #query and download the image from the internet
    gis = GoogleImagesSearch('AIzaSyCR0DCaMCyhKNU8Sxnlg9d5gDoRfGqlF4E', '016040578520524185149:aj1ixvinhes')

    _search_params = {
        'q': query,
        'num': 10,
        'fileType': 'jpg'
    }

    gis.search(search_params=_search_params)
    for image in gis.results():
        image.download("C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\chat page car")

    fnames = os.listdir('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\chat page car\\')
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
            image.download("C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\chat page car")

        fnames = os.listdir('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\chat page car\\')
        return fnames[0]

def predict(car_dict):
    error = 100

    now = datetime.datetime.now()
    datetime_year = int(now.strftime("%Y"))
    datetime_month = int(now.strftime("%m"))
    badge = transform_badge(car_dict['badge'])
    make = get_make(car_dict['make'])
    model = get_model(car_dict['model'])
    fuel = get_fuel(car_dict['fuel_type'])
    body = get_body(car_dict['body_type'])
    
    #LOAD MODEL
    pkl_file_badge = open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\models\\LE01-badge_transformed.pkl', 'rb')
    le_badge_transformed = pickle.load(pkl_file_badge) 
    pkl_file_badge.close()

    pkl_file_coordinates = open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\models\\LE01-coordinates2city.pkl', 'rb')
    le_coordinates2city = pickle.load(pkl_file_coordinates) 
    pkl_file_coordinates.close()
    
    filename = 'C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\models\\M01-RandomForestRegressor.sav'
    regressor = pickle.load(open(filename, 'rb'))
    
    #PREDICT
    badge = int(le_badge_transformed.transform([badge])[0])
    city = int(le_coordinates2city.transform([car_dict['city']])[0])
    pred = regressor.predict(np.array([make, model, fuel, body, car_dict['year'], car_dict['km'], badge, city, datetime_year, datetime_month]).reshape(1,-1))
    pred1 = round(pred[0]-error)
    pred2 = round(pred[0]+error)
    return str(pred1)+" - "+str(pred2)