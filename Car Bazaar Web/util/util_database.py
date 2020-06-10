import pymysql
import numpy as np


db = pymysql.connect(host='localhost',user='root',passwd='',db='caroogle')      #connect with database
cursor = db.cursor()


#change these func names to say get_x_id
def get_make(make):
    query = ("SELECT dim_make.make_id FROM dim_make WHERE dim_make.make='"+make+"';")
    cursor.execute(query)
    return cursor.fetchall()[0][0]

def get_model(model):
    query = ("SELECT dim_model.model_id FROM dim_model WHERE dim_model.model='"+model+"';")
    cursor.execute(query)
    return cursor.fetchall()[0][0]

def get_fuel(fuel):
    query = ("SELECT dim_fuel_type.fuel_type_id FROM dim_fuel_type WHERE dim_fuel_type.fuel_type='"+fuel+"';")
    cursor.execute(query)
    return cursor.fetchall()[0][0]

def get_body(body):
    query = ("SELECT dim_body_type.body_type_id FROM dim_body_type WHERE dim_body_type.body_type='"+body+"';")
    cursor.execute(query)
    return cursor.fetchall()[0][0]

def is_badge(make, model, badge):
    badges  = all_badges_by_model(make, model)
    return badge in badges

def all_makes():
    try:
        query =  ("SELECT dim_make.make FROM dim_make;")
        cursor.execute(query)
        return [make[0] for make in cursor.fetchall()]
    except:
        return []

def all_models_by_make(make):
    try:
        make_id = get_make(make)
        query = ("SELECT dim_model.model FROM dim_model WHERE dim_model.make_id = '"+str(make_id)+"';")
        cursor.execute(query)
        return [model[0] for model in cursor.fetchall()]
    except:
        return []

def all_badges_by_model(make,model):
    try:
        make_id = get_make(make)
        model_id = get_model(model)
        query =  ("SELECT DISTINCT(ads_fact.badge) FROM ads_fact WHERE ads_fact.make_id='"+str(make_id)+"' AND ads_fact.model_id='"+str(model_id)+"';")
        cursor.execute(query)
        return [badge[0] for badge in cursor.fetchall()]
    except:
        return []

def all_bodies_by_model(make,model):
    try:
        make_id = get_make(make)
        model_id = get_model(model)
        query = ("SELECT dim_body_type.body_type FROM dim_body_type WHERE dim_body_type.body_type_id IN (SELECT ads_fact.body_type_id FROM ads_fact WHERE ads_fact.make_id='"+str(make_id)+"' AND ads_fact.model_id='"+str(model_id)+"');")
        cursor.execute(query)
        return [body_type[0] for body_type in cursor.fetchall()]
    except:
        return []

def all_fuels_by_model(make,model):
    try:
        make_id = get_make(make)
        model_id = get_model(model)
        query = ("SELECT dim_fuel_type.fuel_type FROM dim_fuel_type WHERE dim_fuel_type.fuel_type_id IN (SELECT ads_fact.fuel_type_id FROM ads_fact WHERE ads_fact.make_id='"+str(make_id)+"' AND ads_fact.model_id='"+str(model_id)+"');")
        cursor.execute(query)
        return [body_type[0] for body_type in cursor.fetchall()]
    except:
        return []

#year #not a dropdown
#km driven #not a dropdown (scrollable?)
#city (add column to database)