from typing import Any, Text, Dict, List
# from sqlalchemy import create_engine, Table
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

# Base = declarative_base()
# engine = create_engine("sqlite:///menu_list.db", echo=True)

# class PizzaList(Base):
#     __table__ = Table('pizza_type', Base.metadata, autoload=True, autoload_with=engine)

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

FIELDS_OF_STUDY = ["fizyka","informatyka","matematyka","chemia","biologia","automatyka","zarządzanie"]

class LimitForm(FormAction):
    def name(self)-> Text:
        return "form_limits"

    @staticmethod
    def required_slots(tracker: Tracker) ->  List[Text]:
        return ["field-of-study","course-level","course-type"]
    
    def submit(self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]):
        field_of_study = tracker.get_slot("field-of-study")
        course_level = tracker.get_slot("course-level")
        course_type = tracker.get_slot("course-type")
        limit = 80
        print (f"{field_of_study}:{course_level}:{course_type}")
        msg = "Niestety nie udało mi się znaleźć odpowiedzi na twoje pytanie. Spróbuj inaczej zadać pytanie lub sprawdż limity na stronie hddp://calkowicie_poprawny_i_prawdziwy_link_do_strony_z_limitami.hlmt"
        if field_of_study in FIELDS_OF_STUDY:
            msg = f"Limit miejsc na kierunku {field_of_study}"

        dispatcher.utter_message(msg)

        return [AllSlotsReset()]

    def slot_mappings(self) -> Dict[Text,Any]:
        return {"field-of-study": self.from_entity(entity="field-of-study", intent=["get_field_of_study"]),"course_level": self.from_entity(entity="course-level", intent=["get_course_level"]),"course-type": self.from_entity(entity="course-type", intent=["get_course_type"])}