## basic
* greet
    - utter_greet
* ask_about_me
    - utter_ask_about_me
* goodbye
    - utter_goodbye

## basic + ask_skill_list
* greet
    - utter_greet
* ask_about_me
    - utter_ask_about_me
* ask_skill_list
    - utter_ask_skill_list
* goodbye
    - utter_goodbye

## ask_about_limits
* greet
    - utter_greet
* ask_field_of_study_limits{"field_of_study":"informatyka","course_level":"level1","course_type":"stacjonarne"}
    - form_ask_limits
    - form{"name":"form_ask_limits"}
    - form{"name":null}
*  goodbye
    - utter_goodbye
