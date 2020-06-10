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

def save_dict(make, model, fuel, body, year, mileage, badge, city):

    car_dict = {}
    car_dict['make'] = make
    car_dict['model'] = model
    car_dict['fuel_type'] = fuel
    car_dict['body_type'] = body
    car_dict['year'] = year
    car_dict['mileage'] = mileage
    car_dict['badge'] = badge
    car_dict['city'] = city

    return car_dict


def fetch_img(query):

    #remove existing images
    files = glob.glob('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\chat page car\\*')
    for f in files:
        os.remove(f)

    #query and download the image from the internet
    gis = GoogleImagesSearch('xyz', 'abc')

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

#takes list of dictionaries and outputs a list of predictions

def predict(car_dict): #list

    #LOAD MODEL
    pkl_file_badge = open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\models\\LE01-badge_transformed.pkl', 'rb')
    le_badge_transformed = pickle.load(pkl_file_badge) 
    pkl_file_badge.close()

    pkl_file_coordinates = open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\models\\LE01-coordinates2city.pkl', 'rb')
    le_coordinates2city = pickle.load(pkl_file_coordinates) 
    pkl_file_coordinates.close()
    
    filename = 'C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\models\\M01-RandomForestRegressor.sav'
    regressor = pickle.load(open(filename, 'rb'))

    error = 100

    now = datetime.datetime.now()
    datetime_year = int(now.strftime("%Y"))
    datetime_month = int(now.strftime("%m"))

    try:
    
        X_test = []

        for car in car_dict:
            badge = transform_badge(car['badge'])
            badge = int(le_badge_transformed.transform([badge])[0])
            make = get_make(car['make'])
            model = get_model(car['model'])
            fuel = get_fuel(car['fuel_type'])
            body = get_body(car['body_type'])
            city = int(le_coordinates2city.transform([car['city']])[0])

            X_test.append([make, model, fuel, body, int(car['year']), int(car['mileage']), badge, city, datetime_year, datetime_month])

        X_test = numpy.array(X_test)

        preds = regressor.predict(X_test)
        results = []
        for pred in preds:
            pred1 = round(pred-error)
            pred2 = round(pred+error)
            results.append(str(pred1)+" - "+str(pred2))

    except:
        results = ["N/A. Incorrect information."]
        preds = [0]

    return results, preds
