## basic story
* greet
    -   utter_greet
* goodbye
    -   utter_goodbye

## basic story + about_me
* greet
    -   utter_greet
* about_me
    -   utter_about_me
* goodbye
    -   utter_goodbye

## restaurant_search
* greet
    - utter_greet
* search_provider{"facility_type":"restaurant","location":"Rzeszów"}
    - action_facility_search
    - slot {"address":"Hetmańska 53/67"}
* goodbye
    - utter_goodbye

## restaurant_search + ask location
* greet
    - utter_greet
* search_provider{"facility_type":"restaurant"}
    - utter_ask_location
* inform{"location":"Rzeszów"}
    - action_facility_search
    - slot {"address":"Hetmańska 53/67"}
* goodbye
    - utter_goodbye

## order_pizza
* greet
    - utter_greet
* order{"pizza_type":"americana", "pizza_size":"large"}
    - action_save_order
* goodbye
    - utter_goodbye

## order_pizza + pizza_type
* greet
    - utter_greet
* order{"pizza_size":"large"}
    - utter_ask_for_pizza_type
* get_type{"pizza_type":"americana"}
    - action_save_order
* goodbye
    - utter_goodbye

## order_pizza + pizza_size
* greet
    - utter_greet
* order{"pizza_type":"americana"}
    - utter_ask_for_pizza_size
* get_size{"pizza_size":"large"}
    - action_save_order
* goodbye
    - utter_goodbye

## order_pizza + pizza_size + pizza_type
* greet
    - utter_greet
* order
    - utter_ask_for_pizza_size
* get_size{"pizza_size":"large"}
    - utter_ask_for_pizza_type
* get_type{"pizza_type":"americana"}
    - action_save_order
* goodbye
    - utter_goodbye

## menu
* greet
    - utter_greet
* menu
    - action_get_menu
* goodbye
    - utter_goodbye