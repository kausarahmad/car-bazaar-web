import pickle
import numpy as np
import re
import datetime
from flask import Flask, render_template, request

import sys
sys.path.insert(1, "C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\")
from util_database import *
from util_app import *

from google_images_search import GoogleImagesSearch
import os
import glob

import string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        make = request.form['make'].capitalize()
        model = request.form['model'].capitalize()
        badge = request.form['badge'].capitalize()
        fuel = request.form['fuel'].capitalize()
        body = request.form['body'].capitalize()
        mileage = request.form['km']
        year = request.form['year']
        city = string.capwords(request.form['city'])

        imgfilename = fetch_img(make+" "+model+" "+badge+" "+year+" "+body+" "+fuel)

        car_dict = save_dict(make, model, fuel, body, year, mileage, badge, city)

        price_range, pric = predict([car_dict])

        #save dict
        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        return render_template('chat.html', imgcar = "img/chat page car/" + imgfilename, price = price_range[0], make = make, model = model, 
            badge = badge, fuel = fuel, body = body, km = mileage, year = year, city = city)
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
