from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

FIELDS_OF_STUDY = ["fizyka", "informatyka", "matematyka",
                   "chemia", "biologia", "automatyka", "zarządzanie"]

Base = declarative_base()
engine = create_engine("sqlite:///db/uczelnia.db", echo=True)

class ListOfStudyFields(Base):
    __table__ = Table('przedmioty', Base.metadata, autoload=True, autoload_with=engine)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_subject_limit(study_field):
    session = Session()

    try:
        question_target = session.query(ListOfStudyFields).filter(
            ListOfStudyFields.nazwa == study_field).one()
    except:
        return []

    limit_stat1 = question_target.stacjonarne_S1
    limit_stat2 = question_target.stacjonarne_S2
    limit_niestat1 = question_target.stacjonarne_S1
    limit_niestat2 = question_target.stacjonarne_S2
    session.close()
    return {"limit_stat1": limit_stat1, "limit_stat2": limit_stat2, "limit_niestat1": limit_niestat1, "limit_niestat2": limit_niestat2}


def prepare_message(field_of_study, course_level, course_type, limit):
    if course_level is None and course_type == "stacjonarne":
        if limit['limit_stat1'] is None:
            course_level = "level2"
        if limit['limit_stat2'] is None:
            course_level = "level1"

    if course_level is None and course_type == "niestacjonarne":
        if limit['limit_niestat1'] is None:
            course_level = "level2"
        if limit['limit_niestat2'] is None:
            course_level = "level1"

    if course_type is None and course_level == "level1":
        if limit['limit_stat1'] is None:
            course_type = "niestacjonarne"
        if limit['limit_niestat1'] is None:
            course_type = "stacjonarne"

    if course_type is None and course_level == "level2":
        if limit['limit_stat2'] is None:
            course_type = "niestacjonarne"
        if limit['limit_niestat2'] is None:
            course_type = "stacjonarne"


    print_type = ""
    print_level = ""
    print_limit = 0
    if course_level == "level1" and course_type == "stacjonarne":
        print_type = "stacjonarnych"
        print_level = "pierwszego stopnia"
        print_limit = limit['limit_stat1']
    elif course_level == "level2" and course_type == "stacjonarne":
        print_type = "stacjonarnych"
        print_level = "drugiego stopnia"
        print_limit = limit['limit_stat2']
    elif course_level == "level1" and course_type == "niestacjonarne":
        print_type = "niestacjonarnych"
        print_level = "pierwszego stopnia"
        print_limit = limit['limit_niestat1']
    elif course_level == "level2" and course_type == "niestacjonarne":
        print_type = "niestacjonarnych"
        print_level = "drugiego stopnia"
        print_limit = limit['limit_niestat2']

    msg = f"Na {print_type} studiach {print_level} na kierunku {field_of_study} limit miejsc wynosi {print_limit}"
    return msg


class LimitForm(FormAction):
    def name(self) -> Text:
        return "form_limits"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        study_field = tracker.get_slot("field-of-study")

        if study_field not in FIELDS_OF_STUDY:
            return []

        limits = get_subject_limit(study_field)

        if limits['limit_niestat1'] is None and limits['limit_niestat2'] is None:
            return ["field-of-study", "course-level"]
        elif limits['limit_stat2'] is None and limits['limit_niestat2'] is None:
            return ["field-of-study", "course-type"]
        elif limits['limit_stat1'] is None and limits['limit_stat2'] is None:
            return ["field-of-study", "course-level"]
        else:
            return ["field-of-study", "course-level", "course-type"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        try:
            field_of_study = tracker.get_slot("field-of-study")
            course_level = tracker.get_slot("course-level")
            course_type = tracker.get_slot("course-type")
        except:
            pass

        limit = get_subject_limit(field_of_study)

        msg = prepare_message(field_of_study, course_level, course_type, limit)

        dispatcher.utter_message(msg)

        return [AllSlotsReset()]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"field-of-study": self.from_entity(entity="field-of-study", intent=["get_field_of_study"]), "course_level": self.from_entity(entity="course-level", intent=["get_course_level"]), "course-type": self.from_entity(entity="course-type", intent=["get_course_type"])}
