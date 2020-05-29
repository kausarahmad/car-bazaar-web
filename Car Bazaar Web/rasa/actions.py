# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
from collections import defaultdict
#
from fpdf import FPDF
#
car = defaultdict(lambda:"")
#
car['make'] = 'Toyota'
car['model'] = 'Corolla'
car['badge'] = 'Altis'
car['body'] = 'SUV'
car['fuel'] = 'Petrol'
car['year'] = 2003
car['km'] = 0
car['city'] = 'Melbourne'
#
class ActionSave(Action):
    def name(self) -> Text:
        return "action_save"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=16)
        pdf.image("C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\img\\logo\\logo-small.png", x = 15, y = 5, w = 20)
        pdf.ln(1)
        pdf.cell(200, 10, txt="Here's the conversation you had with us!", ln=2, align="C")
        pdf.set_font("Helvetica", size=12)
        pdf.ln(6)
        line = 6
        for event in tracker.events:
            if event.get("event") == "user":
                print("You:", event.get("text"))
                pdf.cell(200, 5, txt="You: "+event.get("text"), ln=line, align="L")
            elif event.get("event") == "bot":
                print("Car Bazaar:", event.get("text"))
                pdf.cell(200, 5, txt="Car Bazaar: "+event.get("text"), ln=line, align="L")

            line+=1

        pdf.output("CarBazaar.pdf")

        dispatcher.utter_message(text="Your conversation has been saved and downloaded for you to use")

        return []
