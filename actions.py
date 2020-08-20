from typing import Any, Text, Dict, List
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

Base = declarative_base()
engine = create_engine("sqlite:///db/uczelnia.db", echo=True)

class ListOfStudyFields(Base):
    __table__ = Table('przedmioty', Base.metadata, autoload=True, autoload_with=engine)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

FIELDS_OF_STUDY = ["fizyka","informatyka","matematyka","chemia","biologia","automatyka","zarządzanie"]

def get_subject_limits(study_field):
    session = Session()
    question_target = session.query(ListOfStudyFields).filter(ListOfStudyFields.nazwa == study_field).one()
    limit_stat1 = question_target.stacjonarne_S1
    limit_stat2 = question_target.stacjonarne_S2
    limit_niestat1 = question_target.stacjonarne_S1
    limit_niestat2 = question_target.stacjonarne_S2
    return [limit_stat1,limit_stat2,limit_niestat1,limit_niestat2]

class LimitForm(FormAction):
    def name(self)-> Text:
        return "form_limits"

    @staticmethod
    def required_slots(tracker: Tracker) ->  List[Text]:
        study_field = tracker.get_slot("field-of-study")
        if study_field not in FIELDS_OF_STUDY:
            return []

        limit_stat1,limit_stat2,limit_niestat1,limit_niestat2 = get_subject_limits(study_field)

        if limit_niestat1 is None and limit_niestat2 is None:
            return ["field-of-study","course-level"]
        elif limit_stat2 is None and limit_niestat2 is None:
            return ["field-of-study","course-type"]
        elif limit_stat1 is None and limit_stat2 is None:
            return ["field-of-study","course-level"]
        else:
            return ["field-of-study","course-level","course-type"]

    
    def submit(self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]):
        field_of_study = tracker.get_slot("field-of-study")
        course_level = tracker.get_slot("course-level")
        course_type = tracker.get_slot("course-type")

        limit_stat1,limit_stat2,limit_niestat1,limit_niestat2 = get_subject_limits(field_of_study)

        msg = ''
        if course_level == "level1" and course_type=="stacjonarne":
            msg=f"Limit miejsc na kierunku {field_of_study} dla studiów stacjonarnych pierwszgo stopnia to {limit_stat1}"
        elif course_level == "level2" and course_type=="stacjonarne":
            msg=f"Limit miejsc na kierunku {field_of_study} dla studiów stacjonarnych drugiego stopnia to {limit_stat2}"
        elif course_level == "level1" and course_type=="niestacjonarne":
            msg=f"Limit miejsc na kierunku {field_of_study} dla studiów niestacjonarnych pierwszgo stopnia to {limit_niestat1}"
        elif course_level == "level2" and course_type=="niestacjonarne":
            msg=f"Limit miejsc na kierunku {field_of_study} dla studiów stacjonarnych pierwszgo stopnia to {limit_niestat2}"
        else: 
            msg = "Niestety nie udało mi się znaleźć odpowiedzi na twoje pytanie. Spróbuj inaczej zadać pytanie lub sprawdż limity na stronie hddp://calkowicie_poprawny_i_prawdziwy_link_do_strony_z_limitami.hlmt"
        

        dispatcher.utter_message(msg)

        return [AllSlotsReset()]

    def slot_mappings(self) -> Dict[Text,Any]:
        return {"field-of-study": self.from_entity(entity="field-of-study", intent=["get_field_of_study"]),"course_level": self.from_entity(entity="course-level", intent=["get_course_level"]),"course-type": self.from_entity(entity="course-type", intent=["get_course_type"])}