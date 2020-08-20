from typing import Any, Text, Dict, List
# from sqlalchemy import create_engine, Table
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction

# Base = declarative_base()
# engine = create_engine("sqlite:///menu_list.db", echo=True)

# class PizzaList(Base):
#     __table__ = Table('pizza_type', Base.metadata, autoload=True, autoload_with=engine)

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

FIELDS_OF_STUDY = ["fizyka","informatyka","matematyka","chemia","biologia","automatyka","zarządzanie"]

class LimitForm(FormAction):
    def name(self)-> Text:
        return "form_ask_limits"

    @staticmethod
    def required_slots(tracker: Tracker) ->  List[Text]:
        return ["field_of_study","course_level","course_type"]
    
    def slot_mappings(self) -> Dict[Text,Any]:
        return {"field_of_study": self.from_entity(entity="field_of_study", intent=["ask_field_of_study_limits"]),"course_level": self.from_entity(entity="course_level", intent=["ask_field_of_study_limits"]),"course_type": self.from_entity(entity="course_type", intent=["ask_field_of_study_limits"])}
    
    def submit(self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]):
        field_of_study = tracker.get_slot("field_of_study")
        course_level = tracker.get_slot("course_level")
        course_type = tracker.get_slot("course_type")
        limit = 80
        print (f"{field_of_study}:{course_level}:{course_type}")
        msg = "Niestety nie udało mi się znaleźć odpowiedzi na twoje pytanie. Spróbuj inaczej zadać pytanie lub sprawdż limity na stronie hddp://calkowicie_poprawny_i_prawdziwy_link_do_strony_z_limitami.hlmt"
        if field_of_study in FIELDS_OF_STUDY:
            msg = f"Limit miejsc na kierunku {field_of_study}"

        dispatcher.utter_message(msg)

        return []