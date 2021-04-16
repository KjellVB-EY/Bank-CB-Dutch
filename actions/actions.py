# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from pathlib import Path
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

class ActionCheckName(Action):
    
    knowledge=Path("data/names.txt").read_text().split("\n")

    def name(self) -> Text:
        return "check_name_existence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if blob['entity']=='name':
                name=blob['value']
                if name in self.knowledge:
                    tracker.update(SlotSet("name", name))
                    return [SlotSet("name", name)]




class ActionCheckAmount(Action):
    

    def name(self) -> Text:
        return "set_amount_saldo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            for blob in tracker.latest_message['entities']:
                print(tracker.latest_message)
                if blob['entity']=='amount-of-money':
                    value=blob['value']
                    # SlotSet("amount_of_saldo", value)


                    return [SlotSet("amount_of_saldo", value), SlotSet("saldo_filled", True)]
            
            
        # dispatcher.utter_message(text="Hello World!")






# class ActionCheckAmount(Action):
    
#     def name(self) -> Text:
#         return "check_amount"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         slot_value = tracker.get_slot('amount-of-money')
#         if slot_value==None: 
#             dispatcher.utter_message(text='Geef aub het bedrag in dat je wil overschrijven:')

#         # dispatcher.utter_message(text="Hello World!")

#         return []


class ActionSetDate(Action):
    

    def name(self) -> Text:
        return "setDate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if blob['entity']=='date':
                date=blob['value']
                return [SlotSet("date", date)]
            
        # dispatcher.utter_message(text="Hello World!")

        return []


class ActionTakeMoney(Action):
    

    def name(self) -> Text:
        return "subtract_money"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            saldo=tracker.get_slot('amount_of_saldo')
            transfer=tracker.get_slot('amount_of_money')
            new_saldo=saldo-transfer
            dispatcher.utter_message(text=f"Huidig saldo is {new_saldo}")
            return [SlotSet("amount_of_saldo", new_saldo)]





class ResetSlot(Action):

    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("amount_of_money", None),SlotSet("name", None)  ]

class ValidateNameForm(FormValidationAction):
    knowledge=Path("data/names.txt").read_text().split("\n")

    def name(self) -> Text:
        return "validate_transaction_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""

        # If the name is super short, it might be wrong.
        #print(f"First name given = {slot_value} length = {len(slot_value)}")
        # for blob in tracker.latest_message['entities']:
        #     print(tracker.latest_message)
        #     if blob['entity']=='name':
        #         name=blob['value']

        if slot_value in self.knowledge:
            return {"name": slot_value}
            
    
        else:
            dispatcher.utter_message(text=f"The name is not recognized in the list of contacts, please check if the name is spelled correct")
            return {"name": None}


    def validate_amount_of_money(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""

        # If the name is super short, it might be wrong.
        #print(f"First name given = {slot_value} length = {len(slot_value)}")
        # for blob in tracker.latest_message['entities']:
        #     print(tracker.latest_message)
        #     if blob['entity']=='name':
        #         name=blob['value']
        if slot_value <= tracker.get_slot('amount_of_saldo'):
            
            new_saldo=tracker.get_slot('amount_of_saldo')-slot_value
            # dispatcher.utter_message(text=f"Huidig saldo is {new_saldo}")
            return {"amount_of_money": slot_value}
            
    
        else:
            dispatcher.utter_message(text=f"Saldo ontoereikend")
            return {"name": None}

    # def validate_last_name(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     """Validate `last_name` value."""

    #     # If the name is super short, it might be wrong.
    #     print(f"Last name given = {slot_value} length = {len(slot_value)}")
    #     if len(slot_value) <= 2:
    #         dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
    #         return {"last_name": None}
    #     else:
    #         return {"last_name": slot_value}
