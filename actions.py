from typing import Any, Text, Dict, List
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

Base = declarative_base()
engine = create_engine("sqlite:///menu_list.db", echo=True)

class PizzaList(Base):
    __table__ = Table('pizza_type', Base.metadata, autoload=True, autoload_with=engine)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_facility_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        facility = tracker.get_slot("facility_type")
        address = "Hetmańska 99/45"

        dispatcher.utter_message(
            "Here is the address of the {}:{}".format(facility, address)
        )

        return [SlotSet("address", address)]


class ActionSaveOrder(Action):
    def name(self) -> Text:
        return "action_save_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        pizza_type = tracker.get_slot("pizza_type")
        pizza_size = tracker.get_slot("pizza_size")

        dispatcher.utter_message("Order summary: {} {}".format(pizza_size, pizza_type))

        return []


class ActionGetMenuList(Action):
    def name(self) -> Text:
        return "action_get_menu"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        menu = session.query(PizzaList).all()
        print(menu)

        dispatcher.utter_message("Menu:{}".format(menu))
        session.close()
        return []
