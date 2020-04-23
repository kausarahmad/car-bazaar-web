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
#
class ActionSave(Action):
#
    def name(self) -> Text:
        return "action_save"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        for event in tracker.events:
            if event.get("event") == "user":
                print("You:", event.get("text"))
            elif event.get("event") == "bot":
                print("Car Bazaar:", event.get("text"))

        dispatcher.utter_message(text="Your conversation has been saved and downloaded for you to use")

        return []
