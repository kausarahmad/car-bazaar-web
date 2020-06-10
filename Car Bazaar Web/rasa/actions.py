# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
from collections import defaultdict
#
from fpdf import FPDF
#
import sys
sys.path.insert(1, "C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\")

from util_database import *
from util_app import *

import numpy as np
import string

with open("C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\cities.txt", "rb") as fp:   #loading cities
  cities = pickle.load(fp)

pdfdata = []

class ActionSave(Action):
    def name(self) -> Text:
        return "action_save"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=16)
        pdf.image("C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\logo-small.png", x = 15, y = 5, w = 20)
        pdf.ln(1)
        pdf.cell(200, 10, txt="Here's the conversation you had with us!", ln=2, align="C")
        pdf.set_font("Helvetica", size=12)
        pdf.ln(6)
        line = 6

        for conv in pdfdata:
            pdf.cell(200, 5, txt="You: "+conv['user'], ln=line, align="L")
            line+=1
            for botmsg in conv['bot']:
                pdf.cell(200, 5, txt="Car Bazaar: "+botmsg, ln=line, align="L")
                line+=1

        pdf.output("CarBazaar.pdf")

        dispatcher.utter_message(text="Your conversation has been saved and downloaded for you to use.")

        return []

class ActionChangeMake(Action):
    def name(self) -> Text:
        return "action_change_make"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_make = next(tracker.get_latest_entity_values('make'), "").capitalize()

        if (new_make == ""):
            dispatcher.utter_message(text="Sorry, I don't have information about this make. Please ask me about another.")
            return []

        car_dict['make'] = new_make

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        models = all_models_by_make(car_dict['make'])

        if (new_make.upper() == "MCLAREN"):
            models = models[-11:]

        dispatcher.utter_message(text="Your car has been changed to a "+car_dict['make']+".")

        botmsg = ["Your car has been changed to a "+car_dict['make']+"."]

        if (len(models) >= 5):
            dispatcher.utter_message(text="Would you like to change the model of the car to a "+", ".join(models[0:4])+" or "+models[-1]+"?")
            botmsg.append("Would you like to change the model of the car to a \n"+", ".join(models[0:4])+" or "+models[-1]+"?")
        elif (len(models) >= 2):
            dispatcher.utter_message(text="Try changing the model of the car to a "+models[0]+" or "+models[1]+".")
            botmsg.append("Try changing the model of the car to a "+models[0]+" or "+models[1]+".")
        elif (len(models) == 1):
            dispatcher.utter_message(text="Try changing the model of the car to a "+models[0]+".")
            botmsg.append("Try changing the model of the car to a "+models[0]+".")
        elif (len(models) == 0):
            dispatcher.utter_message(text="Sorry, I don't have information about models of this brand.")
            botmsg.append("Sorry, I don't have information about models of this brand.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionChangeModel(Action):
    def name(self) -> Text:
        return "action_change_model"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_model = next(tracker.get_latest_entity_values('model'), "")

        if (new_model == ""):
            dispatcher.utter_message(text="Sorry, I don't have information about this model. Please ask me about another.")
            return []

        car_dict['model'] = new_model

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        badges = all_badges_by_model(car_dict['make'], car_dict['model'])

        dispatcher.utter_message(text="Your car has been changed to a "+car_dict['make']+" "+car_dict['model']+".")
        botmsg = ["Your car has been changed to a "+car_dict['make']+" "+car_dict['model']+"."]

        if (len(badges) >= 5):
            dispatcher.utter_message(text="You might find a cheaper car in a different specification such as \n"+", ".join(badges[0:4])+" or "+badges[-1]+"?")
            botmsg.append("You might find a cheaper car in a different specification such as "+", ".join(badges[0:4])+" or "+badges[-1]+"?")
        elif (len(badges) >= 2):
            dispatcher.utter_message(text="Do you want to change the badge of the car to a "+badges[0]+" or "+badges[1]+"?")
            botmsg.append("Do you want to change the badge of the car to a "+badges[0]+" or "+badges[1]+"?")
        elif (len(badges) == 1):
            dispatcher.utter_message(text="Try changing the specifications of the car to a "+badges[0]+".")
            botmsg.append("Try changing the specifications of the car to a "+badges[0]+".")
        elif (len(badges) == 0):
            dispatcher.utter_message(text="Try asking which city this car is cheaper in.")
            botmsg.append("Try asking which city this car is cheaper in.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionChangeBadge(Action):
    def name(self) -> Text:
        return "action_change_badge"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_badge = next(tracker.get_latest_entity_values('badge'), "")

        if (new_badge == ""):
            dispatcher.utter_message(text="Sorry, I don't have information about this spec. Please ask me about another.")
            return []

        car_dict['badge'] = new_badge

        price_range, price = predict([car_dict])

        bodies = all_bodies_by_model(car_dict['make'], car_dict['model'])

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        dispatcher.utter_message(text="I updated the specifications of your car.")
        dispatcher.utter_message(text="A "+car_dict['make']+" "+car_dict['model']+" "+car_dict['badge']+" usually sells for $"+price_range[0]+".")

        botmsg = ["A "+car_dict['make']+" "+car_dict['model']+" "+car_dict['badge']+"\n usually sells for $"+price_range[0]+"."]

        if (len(bodies) >= 5):
            dispatcher.utter_message(text="Changing the car to a different body type ("+", ".join(bodies[0:4])+" or "+bodies[-1]+") might be more economical.")
            botmsg.append("Changing the car to a different body type \n("+", ".join(bodies[0:4])+" or "+bodies[-1]+") might be more economical.")
        elif (len(bodies) >= 2):
            dispatcher.utter_message(text="Want to see if the same car is cheaper in another body type? Ask me to change the body to a "+bodies[0]+" or "+bodies[1]+".")
            botmsg.append("Want to see if the same car is cheaper in another body type? \nAsk me to change the body to a "+bodies[0]+" or "+bodies[1]+".")
        elif (len(bodies) == 1):
            dispatcher.utter_message(text="You might find a better price if you change the car to a "+bodies[0]+".")
            botmsg.append("You might find a better price if you change the car to a "+bodies[0]+".")
        elif (len(bodies) == 0):
            dispatcher.utter_message(text="Try asking which city this car is cheaper in.")
            botmsg.append("Try asking which city this car is cheaper in.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionChangeBodyType(Action):
    def name(self) -> Text:
        return "action_change_body_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_body_type = next(tracker.get_latest_entity_values('body_type'), "")

        if (new_body_type == ""):
            dispatcher.utter_message(text="Sorry, I don't have information about this body type. Please ask me about another.")
            return []

        car_dict['body_type'] = new_body_type

        price_range, price = predict([car_dict])

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        dispatcher.utter_message(text="I changed the body type of your car to a "+car_dict['body_type']+".")
        botmsg = ["I changed the body type of your car to a "+car_dict['body_type']+"."]
        dispatcher.utter_message(text="A "+car_dict['make']+" "+car_dict['model']+" "+car_dict['badge']+" "+car_dict['body_type']+" might be for $"+price_range[0]+".")
        botmsg.append("A "+car_dict['make']+" "+car_dict['model']+" "+car_dict['badge']+" "+car_dict['body_type']+"\n might be for $"+price_range[0]+".")
        dispatcher.utter_message(text="Want to find out if an older or newer model of this car is more affordable? Ask me to change the car year.")
        botmsg.append("Want to find out if an older or newer model of this car is more affordable? Ask me to change the car year.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionChangeFuelType(Action):
    def name(self) -> Text:
        return "action_change_fuel_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_fuel_type = next(tracker.get_latest_entity_values('fuel_type'), "")

        if (new_fuel_type == ""):
            dispatcher.utter_message(text="Sorry, I don't have information about this fuel. Please ask me about another.")
            return []

        car_dict['fuel_type'] = new_fuel_type

        price_range, price = predict([car_dict])

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        dispatcher.utter_message(text="A "+car_dict['make']+" "+car_dict['model']+" running on "+car_dict['fuel_type']+" would cost around $"+price_range[0]+".")
        botmsg = ["A "+car_dict['make']+" "+car_dict['model']+" running on "+car_dict['fuel_type']+" \nwould cost around $"+price_range[0]+"."]
        dispatcher.utter_message(text="Are you wondering how mileage affects price? Ask me to change your mileage preference.")
        botmsg.append("Are you wondering how mileage affects price? Ask me to change your mileage preference.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionChangeYear(Action):
    def name(self) -> Text:
        return "action_change_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_year = next(tracker.get_latest_entity_values('year'), "")

        if (new_year == ""):
            dispatcher.utter_message(text="Sorry, I don't understand. Please ask me to change the car year again.")
            return []

        car_dict['year'] = new_year

        price_range, price = predict([car_dict])

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        dispatcher.utter_message(text="I changed the model year of your car to "+str(car_dict['year'])+".")
        botmsg = ["I changed the model year of your car to "+str(car_dict['year'])+"."]
        dispatcher.utter_message(text="A "+car_dict['make']+" "+car_dict['model']+" from the year "+str(car_dict['year'])+" is usually priced at $"+price_range[0]+".")
        botmsg.append("A "+car_dict['make']+" "+car_dict['model']+" from the year "+str(car_dict['year'])+" \nis usually priced at $"+price_range[0]+".")
        dispatcher.utter_message(text="You might find a cheaper car in a different city like Adelaide.")
        botmsg.append("You might find a cheaper car in a different city like Adelaide.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionChangeCity(Action):
    def name(self) -> Text:
        return "action_change_city"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_city = string.capwords(next(tracker.get_latest_entity_values('city'), ""))

        if (new_city == ""):
            dispatcher.utter_message(text="Sorry, I don't have information about this city. Please ask me about another.")
            return []

        car_dict['city'] = new_city

        price_range, price = predict([car_dict])

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        dispatcher.utter_message(text="Your desired car would cost between $"+price_range[0]+" in "+car_dict['city']+".")
        botmsg = ["Your desired car would cost between $"+price_range[0]+" in "+car_dict['city']+"."]
        dispatcher.utter_message(text="Not satisfied with this price range? Try changing the model of your car.")
        botmsg.append("Not satisfied with this price range? Try changing the model of your car.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

#NEED TO error proof predict function
class ActionChangeMileage(Action):
    def name(self) -> Text:
        return "action_change_mileage"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        new_mileage = next(tracker.get_latest_entity_values('mileage'), "")

        if (new_mileage == ""):
            dispatcher.utter_message(text="Sorry, I don't understand. Please ask me to change the mileage (in km) again.")
            return []

        car_dict['mileage'] = new_mileage

        price_range, price = predict([car_dict])

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'wb') as f:
            pickle.dump(car_dict, f, pickle.HIGHEST_PROTOCOL)

        dispatcher.utter_message(text="This car, with mileage "+car_dict[mileage]+", usually costs between $"+price_range[0]+".")
        botmsg = ["This car, with mileage "+car_dict[mileage]+", usually costs between $"+price_range[0]+"."]
        dispatcher.utter_message(text="You might find a cheaper car in a different city like Castle Hill.")
        botmsg.append("You might find a cheaper car in a different city like Castle Hill.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionListCheapCity(Action):
    def name(self) -> Text:
        return "action_list_cheap_city"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        #print("cities:",cities)
        car_dict_list = []
        for city in cities:
            car_dict['city'] = city
            #print(car_dict['city'])
            car_dict_list.append(car_dict)
        #print(car_dict_list)
        price_ranges, prices = predict(car_dict_list)

        sorted_prices, sorted_price_ranges, sorted_cities = (list(t) for t in zip(*sorted(zip(prices, price_ranges, cities))))

        dispatcher.utter_message(text="This car is cheapest in "+", ".join(sorted_cities[20:25])+", and "+sorted_cities[25]+".")
        botmsg = ["This car is cheapest in "+", ".join(sorted_cities[20:25])+", and "+sorted_cities[25]+"."]
        dispatcher.utter_message(text="Would you like to change the city to see how the price of your car changes?")
        botmsg.append("Would you like to change the city to see how the price of your car changes?")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionListBadge(Action):
    def name(self) -> Text:
        return "action_list_badge"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        badges = all_badges_by_model(car_dict['make'], car_dict['model'])

        botmsg = []

        if (len(badges)!=0):
            dispatcher.utter_message(text="Some of the specs that this "+car_dict['make']+" "+car_dict['model']+" comes in are:")
            botmsg.append("Some of the specs that this "+car_dict['make']+" "+car_dict['model']+" comes in are:")
            dispatcher.utter_message(text=', '.join(badges[:-1])+", and "+badges[-1]+".")
            botmsg.append(', '.join(badges[:-1])+", and "+badges[-1]+".")
            dispatcher.utter_message(text="Ask me to change the specs of your car to see how it affects price.")
            botmsg.append("Ask me to change the specs of your car to see how it affects price.")
        else:
            dispatcher.utter_message(text="Sorry, I don't have information about the specs of this car.")
            botmsg.append("Sorry, I don't have information about the specs of this car.")
            dispatcher.utter_message(text="Not satisfied with this price range? Try changing the model of your car.")
            botmsg.append("Not satisfied with this price range? Try changing the model of your car.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionListBody(Action):
    def name(self) -> Text:
        return "action_list_body"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        bodies = all_bodies_by_model(car_dict['make'], car_dict['model'])

        botmsg = []

        if (len(bodies) >= 5):
            dispatcher.utter_message(text="Some of the body styles that this "+car_dict['make']+" "+car_dict['model']+" comes in are:")
            botmsg.append("Some of the body styles that this "+car_dict['make']+" "+car_dict['model']+" comes in are:")
            dispatcher.utter_message(text=", ".join(bodies[0:4])+", and "+bodies[-1]+".")
            botmsg.append(", ".join(bodies[0:4])+", and "+bodies[-1]+".")
        elif (len(bodies) >= 2):
            dispatcher.utter_message(text="Some of the body styles that this "+car_dict['make']+" "+car_dict['model']+" comes in are "+bodies[0]+" and "+bodies[1]+".")
            botmsg.append("Some of the body styles that this "+car_dict['make']+" "+car_dict['model']+" comes in are "+bodies[0]+" and "+bodies[1]+".")
        elif (len(bodies) == 1):
            dispatcher.utter_message(text="This "+car_dict['make']+" "+car_dict['model']+" is available as a "+bodies[0]+".")
            botmsg.append("This "+car_dict['make']+" "+car_dict['model']+" is available as a "+bodies[0]+".")
        elif (len(bodies) == 0):
            dispatcher.utter_message(text="I don't have information about the body styles of this car.")
            botmsg.append("I don't have information about the body styles of this car.")

        dispatcher.utter_message(text="Ask me to change the body style of your car to see how it affects price.")
        botmsg.append("Ask me to change the body style of your car to see how it affects price.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionListModel(Action):
    def name(self) -> Text:
        return "action_list_model"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        models = all_models_by_make(car_dict['make'])

        botmsg = []

        if (len(models) >= 5):
            dispatcher.utter_message(text="Some of the models that this "+car_dict['make']+" comes in are:")
            botmsg.append("Some of the models that this "+car_dict['make']+" comes in are:")
            dispatcher.utter_message(text=", ".join(models[0:4])+", and "+models[-1]+".")
            botmsg.append(", ".join(models[0:4])+", and "+models[-1]+".")
        elif (len(models) >= 2):
            dispatcher.utter_message(text="Some of the models that this "+car_dict['make']+" comes in are "+models[0]+" and "+models[1]+".")
            botmsg.append("Some of the models that this "+car_dict['make']+" comes in are "+models[0]+" and "+models[1]+".")
        elif (len(models) == 1):
            dispatcher.utter_message(text="The only model that is available with this "+car_dict['make']+" is a "+models[0]+".")
            botmsg.append("The only model that is available with this "+car_dict['make']+" is a "+models[0]+".")
        elif (len(models) == 0):
            dispatcher.utter_message(text="Sorry, I don't have information about models of this brand.")
            botmsg.append("Sorry, I don't have information about models of this brand.")

        dispatcher.utter_message(text="Ask me to change the model of your car to see how it affects price.")
        botmsg.append("Ask me to change the model of your car to see how it affects price.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionListFuel(Action):
    def name(self) -> Text:
        return "action_list_fuel"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        fuels = all_fuels_by_model(car_dict['make'], car_dict['model'])

        botmsg = []

        if (len(fuels) >= 3):
            dispatcher.utter_message(text="This "+car_dict['make']+" "+car_dict['model']+" can run on:")
            botmsg.append("This "+car_dict['make']+" "+car_dict['model']+" can run on:")
            dispatcher.utter_message(text=", ".join(fuels[0:2])+", and "+fuels[-1]+".")
            botmsg.append(", ".join(fuels[0:2])+", and "+fuels[-1]+".")
        elif (len(fuels) >= 2):
            dispatcher.utter_message(text="This "+car_dict['make']+" "+car_dict['model']+" can run on "+fuels[0]+" and "+fuels[1]+".")
            botmsg.append("This "+car_dict['make']+" "+car_dict['model']+" can run on "+fuels[0]+" and "+fuels[1]+".")
        elif (len(fuels) == 1):
            dispatcher.utter_message(text="The only fuel that this "+car_dict['make']+" "+car_dict['model']+" can run on is "+fuels[0]+".")
            botmsg.append("The only fuel that this "+car_dict['make']+" "+car_dict['model']+" can run on is "+fuels[0]+".")
        elif (len(fuels) == 0):
            dispatcher.utter_message(text="Sorry, I don't have information about this car's fuel types.")
            botmsg.append("Sorry, I don't have information about this car's fuel types.")

        dispatcher.utter_message(text="Ask me to change the fuel type of your car to see how it affects price.")
        botmsg.append("Ask me to change the fuel type of your car to see how it affects price.")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionListCheapBadge(Action):
    def name(self) -> Text:
        return "action_list_cheap_badge"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        badges = all_badges_by_model(car_dict['make'], car_dict['model'])

        car_dict_list = []
        for badge in badges:
            car_dict['badge'] = badge
            car_dict_list.append(car_dict)

        price_ranges, prices = predict(car_dict_list)

        sorted_prices, sorted_price_ranges, sorted_badges = (list(t) for t in zip(*sorted(zip(prices, price_ranges, badges))))

        dispatcher.utter_message(text="This car is cheapest with the specs "+", ".join(sorted_badges[:4])+", and "+sorted_badges[5]+".")
        botmsg = ["This car is cheapest with the specs "+", ".join(sorted_badges[:4])+", \nand "+sorted_badges[5]+"."]
        dispatcher.utter_message(text="Would you like to change the specifications of your car to see its price?")
        botmsg.append("Would you like to change the specifications of your car to see its price?")

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []

class ActionTellPrice(Action):
    def name(self) -> Text:
        return "action_tell_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\util\\car_dict.pkl', 'rb') as f:
            car_dict = pickle.load(f)

        price_range, price = predict([car_dict])

        dispatcher.utter_message(text="A "+str(car_dict['year'])+" "+car_dict['make']+" "+car_dict['model']+" "+car_dict['badge']+" "+car_dict['body_type']+", mileage "+str(car_dict['mileage'])+"km, running on "+car_dict['fuel_type']+" usually sells for $"+price_range[0]+" in "+car_dict['city']+".")

        botmsg = ["A "+str(car_dict['year'])+" "+car_dict['make']+" "+car_dict['model']+" "+car_dict['badge']+" "+car_dict['body_type']+", mileage "+str(car_dict['mileage'])+"km, \nrunning on "+car_dict['fuel_type']+" usually sells for $"+price_range[0]+" in "+car_dict['city']+"."]

        usermsg = tracker.latest_message['text']
        conv = {}
        conv['user'] = usermsg
        conv['bot'] = botmsg

        pdfdata.append(conv)

        return []