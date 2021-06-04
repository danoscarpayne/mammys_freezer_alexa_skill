# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import json


from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
import ask_sdk_core.utils as ask_utils

from ask_sdk_model import Response, DialogState, Intent
from ask_sdk_model.dialog import ElicitSlotDirective
from ask_sdk_model.dialog.delegate_directive import DelegateDirective

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# mapping for drawers
drawer_map = {1 : 'the top drawer',
             2 : 'the second from top drawer',
             3 : 'the third from top drawer',
             4 : 'big box 1',
             5 : 'big box 2',
             6 : 'the second from bottom drawer',
             7 : 'bottom drawer'}

def age_checker(full_age):
    
    yr_age, age = full_age//365, full_age%365
    
    # Go through conditions
    if age < 14:
        
        stment = '{} days'.format(age)
        
    elif (age >= 14) and (age < 90):
        
        stment = '{} weeks'.format(age//7)
        
    elif (age >= 90) and (age < 365):
        
        stment = '{} months'.format(int(round(age/30, 0)))
        
    else:
        
        stment = ''
        
    if yr_age > 0:
        
        if yr_age == 1:
            
            st_yr = '1 year and '
            
        else:
            
            st_yr = '{} years and '
            
    else:
        
        st_yr = ''
        
    spk_out = st_yr + stment
    
    return spk_out


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can say Hello or Help. Which would you like to try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class LocateFoodIntentHandler(AbstractRequestHandler):
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("locateFood")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        print(handler_input)
        
        slot = ask_utils.request_util.get_slot(handler_input, "food_item")
        
        food_item = slot.value
        
        new_url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/{}'.format(food_item)

        r = requests.get(new_url)
        
        # mapping for drawers
        drawer_map = {1 : 'the top drawer',
                     2 : 'the second from top drawer',
                     3 : 'the third from top drawer',
                     4 : 'big box 1',
                     5 : 'big box 2',
                     6 : 'the second from bottom drawer',
                     7 : 'bottom drawer'}
    
        speech_template = ""
    
        j_put = r.json()
        
        # Logic
        if len(j_put) == 0:
    
            spk_out = 'You have no {} in the freezer'.format(food_item)
    
        else:
    
            speech_template += 'You have {:0.0f} {} in {}'.format(j_put[0].get('qty', 1), j_put[0].get('name', ''), drawer_map.get(j_put[0].get('location')))
    
            if len(j_put) > 1:
    
                for i in range(1, len(j_put)):
                    speech_template += ' and you have {:0.0f} {} in {}'.format(j_put[i].get('qty', 1), j_put[i].get('name', ''), drawer_map.get(j_put[i].get('location')))
    
            spk_out = speech_template
        
        
        
        
        
        return (handler_input.response_builder.speak(spk_out)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response)
      
class checkitemIntentHandler(AbstractRequestHandler):
    
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("checkItemQty")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slot = ask_utils.request_util.get_slot(handler_input, "food_item")
        
        
        food_item = slot.value
        
        new_url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/{}'.format(food_item)

        r = requests.get(new_url)
        
        # mapping for drawers
        drawer_map = {1 : 'the top drawer',
                     2 : 'the second from top drawer',
                     3 : 'the third from top drawer',
                     4 : 'big box 1',
                     5 : 'big box 2',
                     6 : 'the second from bottom drawer',
                     7 : 'bottom drawer'}
    
        speech_template = ""
    
        j_put = r.json()
        
        # Logic
        if len(j_put) == 0:
    
            spk_out = 'You have no {} in the freezer'.format(food_item)
    
        elif len(j_put) >= 2:
            
            spk_out = 'You have '
            
            for i, item in enumerate(j_put):
                
                if i >= 1:
                    
                    spk_out += 'and '
                
                spk_out += '{} {} in {} with id {} '.format(item['qty'], item['name'], drawer_map[item['location']], item['food_id'])
            
            spk_out = spk_out +  ' Which one do you want to select'   
            reprompt = 'Which one do you want to select'
            
            print(handler_input.response_builder.speak(spk_out).ask(reprompt).add_directive(ElicitSlotDirective(
                    updated_intent=Intent(
                        name="selectFoodItem"), 
                    slot_to_elicit="food_id")).response)
            
            return handler_input.response_builder.speak(spk_out).ask(reprompt).add_directive(ElicitSlotDirective(
                    updated_intent=Intent(
                        name="selectFoodItem"), 
                    slot_to_elicit="food_id")).response
            #return SelectFoodIntentHandler.handle(self, handler_input)
                    
        else:
            
            item = j_put[0]
            
            spk_out = 'You have {} of {} in {}'.format(item['qty'], item['name'], drawer_map[item['location']])
            
            session_attr = handler_input.attributes_manager.session_attributes
 
            # Get the slot value from the request and add it to the session 
            # attributes dictionary. Because of the dialog model and dialog 
            # delegation, this code only ever runs when the favoriteColor slot 
            # contains a value, so a null check is not necessary.
            
            food_id = item['food_id']
            session_attr["selected_food"] = food_id
            
        return (handler_input.response_builder
                    .speak(spk_out).response)
            
            
            
            
            
class checkDrawerContentsIntentHandler(AbstractRequestHandler):
    
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("checkDrawerContents")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        #slot = ask_utils.request_util.get_slot(handler_input, "drawer")
        
        drawer_slot = handler_input.request_envelope.request.intent.slots
        
        print(drawer_slot['drawer'].resolutions.resolutions_per_authority)
        
        
        try:
            
            id_check = drawer_slot['drawer'].resolutions.resolutions_per_authority[0].values[0].value.id
            
            #id_check = slot.resolutions.resolutionsPerAuthority[0].values[0].value.id
            
            #ids = [str(x['value']['name']) for x in slot['resolutions']['resolutionsPerAuthority'][0]['values']]
            
            #id_check = ' and '.join(ids)
            
        except:
            
            id_check = 'claremorris'
        
        
        if drawer_slot['drawer'].resolutions:
            
            #key_check = list(slot['resolutions'].keys())[0]
            
            speak_output = "I am in {} in your Freezer.  Lets have a party".format(id_check)#, id_check)
        else:
            # this city was not built on rock'n'roll
            speak_output = "this is not in the Freezer"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response)  
class checkFoodAgeIntentHandler(AbstractRequestHandler):
    
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("checkFoodAgeGeneral")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # mapping for drawers
        drawer_map = {1 : 'the top drawer',
                     2 : 'the second from top drawer',
                     3 : 'the third from top drawer',
                     4 : 'big box 1',
                     5 : 'big box 2',
                     6 : 'the second from bottom drawer',
                     7 : 'bottom drawer'}
    
        old_url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/find_oldest_items'
    
        req_params = {'location' : None,
                 'limit' : None}
    
        a = requests.get(old_url, params=req_params)
        j_resp = a.json()
        
        spoken_reposnse = 'You have '
        
        for i, food in enumerate(j_resp):
            
            # define variables
            food_qty = food['qty']
            food_name = food['name']
            food_location = drawer_map[food['location']]
            food_age = age_checker(food['age'])
            
            if food_qty.is_integer():
                food_qty = int(food_qty)
            else:
                if food_qty < 1:
                    
                    food_qty = str(int(food_qty * 100)) + ' percent of the'
                    
                else:
                    
                    food_qty = food_qty
            if i >= 1:
                
                spoken_reposnse += 'and '
                
            spoken_reposnse += '{} {} in {} for {} '.format(food_qty, food_name, food_location,food_age)

        return (
            handler_input.response_builder
                .speak(spoken_reposnse)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response)
                
class MoveFoodItemIntentHandler(AbstractRequestHandler):
    
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("moveFoodItem")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Get slots
        input_slots = handler_input.request_envelope.request.intent.slots
        
        # needed variables
        food_name = input_slots['food_name'].value
        from_location = input_slots['from_location'].resolutions.resolutions_per_authority[0].values[0].value.id
        to_location = input_slots['to_location'].resolutions.resolutions_per_authority[0].values[0].value.id
        
        
        new_url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/{}'.format(food_name)
        
        print(new_url)

        r = requests.get(new_url)
        
        # response
        json_response = r.json()
        
        print('response is {}'.format(json_response))
        
        # selected items 
        selected_food = [x for x in json_response if x.get('location') == int(from_location)]
        
        print(selected_food)
        
        if len(selected_food) == 1:
            
            selected_ = selected_food[0]
            
            print('dict object is of type {} and is {}'.format(type(selected_), selected_))
            
            # Get any existing attributes from the incoming request
            session_attr = handler_input.attributes_manager.session_attributes
            
            session_attr["food_to_move"] = selected_.get('food_id')
            session_attr["move_destination"] = to_location
            
            # set payload
            payload = {'id' : session_attr["food_to_move"], 'location' : session_attr["move_destination"]}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/move_item'
            
            # make request
            r = requests.put(url, headers=headers, data=payload)
            
            if r.status_code == 200:
                
                session_attr["food_to_move"] = None
                session_attr["move_destination"] = None
            
                speak_output = 'I have moved {} to {}'.format(selected_.get('name'), drawer_map[int(to_location)])
                
            else:
                
                speak_output = 'I encountered a problem as was unable to move {} please try again'.format(selected_['name'])
                
            return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response) 
        
        elif len(selected_food) == 0:
            
            if len(json_response) > 0:
                
                speak_output = 'I don\'t have it in that location. I have'
                
                # loop through
                for i, item in enumerate(json_response):
                    
                    if i >= 1:
                        
                        speak_output += ' and'
                    
                    speak_output += ' {} in location {}'.format(item.get('name'), drawer_map[int(item.get('location'))])
                    
                speak_output += ' If you  want to move one of these items, say move {} from {} to {}'.format(json_response[0].get('name'), drawer_map[int(json_response[0].get('location'))], drawer_map[int(to_location)])
                
            else:
                
                speak_output = 'I cannot find the item you requested'
                
            return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response) 
                
                
        else:
            
            # Access session attributes
            # Get any existing attributes from the incoming request
            session_attr = handler_input.attributes_manager.session_attributes
        
            session_attr["move_destination"] = to_location
            
            # initiate dictionary
            opt_dict  = {}
            
            for i, val in enumerate(selected_food):
                
                opt_dict[str(i + 1)] = {'name' : val.get('name'), 'i.d.' : val.get('food_id'), 'location' : drawer_map[int(val.get('location'))]}
                
            str_dict = json.dumps(opt_dict)
                
            session_attr["move_options"] = opt_dict
            
            speak_output = 'This is ambiguous I have too many items. please select an option. '
            
            for options in session_attr["move_options"].keys():
                
                speak_output += ' option {}, {} in {} with i.d. {}'.format(options, session_attr["move_options"][options]['name'], session_attr["move_options"][options]['location'], session_attr["move_options"][options]['i.d.'])
            
            speak_output += ' please select an option'
            
            reprompt = 'please select an option'

        return (
            handler_input.response_builder.speak(speak_output).ask(reprompt).add_directive(ElicitSlotDirective(
                    updated_intent=Intent(
                        name="selectFoodItem"), 
                    slot_to_elicit="food_option")).response) 
                    
class UpdateFoodItemIntentHandler(AbstractRequestHandler):
    
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("updateItemQty")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Get slots
        input_slots = handler_input.request_envelope.request.intent.slots
        
        # needed variables
        food_name = input_slots['food_name'].value
        from_location = input_slots['drawer'].resolutions.resolutions_per_authority[0].values[0].value.id
        item_qty = input_slots['item_qty'].value
        
        
        new_url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/{}'.format(food_name)
        
        print(new_url)

        r = requests.get(new_url)
        
        # response
        json_response = r.json()
        
        print('response is {}'.format(json_response))
        
        # selected items 
        selected_food = [x for x in json_response if x.get('location') == int(from_location)]
        
        print(selected_food)
        
        if len(selected_food) == 1:
            
            selected_ = selected_food[0]
            
            print('dict object is of type {} and is {}'.format(type(selected_), selected_))
            
            # Get any existing attributes from the incoming request
            session_attr = handler_input.attributes_manager.session_attributes
            
            session_attr["food_to_update"] = selected_.get('food_id')
            session_attr["item_qty"] = item_qty
            
            # set payload
            payload = {'id' : session_attr["food_to_update"], 'qty' : float(session_attr["item_qty"])}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/update_food_qty'
            
            # make request
            r = requests.put(url, headers=headers, data=payload)
            
            if r.status_code == 200:
                
                session_attr["food_to_update"] = None
                session_attr["item_qty"] = None
            
                speak_output = 'I have updated the quantity of {} in {} to {}'.format(selected_.get('name'), drawer_map[int(from_location)], item_qty)
                
            else:
                
                speak_output = 'I encountered a problem as was unable to update {} please try again'.format(selected_['name'])
                
            return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response) 
        
        elif len(selected_food) == 0:
            
            if len(json_response) > 0:
                
                speak_output = 'I don\'t have it in that location. I have'
                
                # loop through
                for i, item in enumerate(json_response):
                    
                    if i >= 1:
                        
                        speak_output += ' and'
                    
                    speak_output += ' {} in location {}'.format(item.get('name'), drawer_map[int(item.get('location'))])
                    
                speak_output += ' If you  want to update one of these items, say update {} from {} to {}'.format(json_response[0].get('name'), drawer_map[int(json_response[0].get('location'))], item_qty)
                
            else:
                
                speak_output = 'I cannot find the item you requested'
                
            return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response) 
                
                
        else:
            
            # Access session attributes
            # Get any existing attributes from the incoming request
            session_attr = handler_input.attributes_manager.session_attributes
        
            session_attr["item_qty"] = item_qty
            
            # initiate dictionary
            opt_dict  = {}
            
            for i, val in enumerate(selected_food):
                
                opt_dict[str(i + 1)] = {'name' : val.get('name'), 'i.d.' : val.get('food_id'), 'location' : drawer_map[int(val.get('location'))]}
                
            str_dict = json.dumps(opt_dict)
                
            session_attr["update_options"] = opt_dict
            
            speak_output = 'This is ambiguous I have too many items. please select an option. '
            
            for options in session_attr["update_options"].keys():
                
                speak_output += ' option {}, {} in {} with i.d. {}'.format(options, session_attr["update_options"][options]['name'], session_attr["update_options"][options]['location'], session_attr["update_options"][options]['i.d.'])
            
            speak_output += ' please select an option'
            
            reprompt = 'please select an option'

        return (
            handler_input.response_builder.speak(speak_output).ask(reprompt).add_directive(ElicitSlotDirective(
                    updated_intent=Intent(
                        name="selectFoodItem"), 
                    slot_to_elicit="food_option")).response) 
class SelectFoodIntentHandler(AbstractRequestHandler):
    """Handler for FavoriteColorIntent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("selectFoodItem")(
            handler_input) and ask_utils.get_dialog_state(
            handler_input=handler_input) == DialogState.COMPLETED
 
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
 
        # Get any existing attributes from the incoming request
        session_attr = handler_input.attributes_manager.session_attributes
        
        
        check_slots = handler_input.request_envelope.request.intent.slots
        print(check_slots)
 
        # Get the slot value from the request and add it to the session 
        # attributes dictionary. Because of the dialog model and dialog 
        # delegation, this code only ever runs when the favoriteColor slot 
        # contains a value, so a null check is not necessary.
        food_option = ask_utils.request_util.get_slot(handler_input, "food_option")
        
        
        if not food_option:
            
            speech_text = "I am sorry, i did not get an option"
            
            return handler_input.response_builder.speak(speech_text).response
             
        else:
            
            if session_attr.get("move_options", None):
            
                move_options = session_attr["move_options"]
                #move_options = json.loads(session_attr["move_options"])
                
                food_id = move_options[food_option.value]['i.d.']
                food_name = move_options[food_option.value]['name']
                to_location = session_attr["move_destination"]
                
                print(food_name, food_id)
                
                
                # set payload
                payload = {'id' : food_id, 'location' : session_attr["move_destination"]}
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/move_item'
                
                # make request
                r = requests.put(url, headers=headers, data=payload)
                
                if r.status_code == 200:
                    
                    session_attr["move_options"] = None
                    session_attr["move_destination"] = None
                
                    speak_output = 'I have moved {} to {}'.format(food_name, drawer_map[int(to_location)])
                    
                else:
                    
                    speak_output = 'I encountered a problem as was unable to move {} please try again'.format(food_name)
                    
                return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response)
                    
            elif session_attr.get("delete_options"):
                
                delete_options = session_attr["delete_options"]
                #move_options = json.loads(session_attr["move_options"])
                
                food_id = delete_options[food_option.value]['i.d.']
                food_name = delete_options[food_option.value]['name']
                location = delete_options[food_option.value]['location']
                
                print(food_name, food_id)
                
                
                # set url 
                url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/delete_item/{}'.format(food_id)
                
                # make request
                r = requests.delete(url)
                
                if r.status_code == 200:
                    
                    session_attr["delete_options"] = None
                
                    speak_output = 'I have removed {} from {}'.format(food_name, location)
                    
                else:
                    
                    speak_output = 'I encountered a problem as was unable to remove {} please try again'.format(food_name)
                    
                return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response)
                    
            elif session_attr.get("update_options"):
                
                update_options = session_attr["update_options"]
                #move_options = json.loads(session_attr["move_options"])
                
                food_id = update_options[food_option.value]['i.d.']
                food_name = update_options[food_option.value]['name']
                item_qty = session_attr["item_qty"]
                
                print(food_name, food_id)
                
                
                # set payload
                payload = {'id' : food_id, 'qty' : float(session_attr["item_qty"])}
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/update_food_qty'
                
                # make request
                r = requests.put(url, headers=headers, data=payload)
                
                if r.status_code == 200:
                    
                    session_attr["update_options"] = None
                    session_attr["item_qty"] = None
                
                    speak_output = 'I have updated {} to {}'.format(food_name, item_qty)
                    
                else:
                    
                    speak_output = 'I encountered a problem as was unable to update {} please try again'.format(food_name)
                    
                return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response)
                    
            else:
                
                speak_output = 'I encountered a problem please try again'.format(food_name)
                    
                return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response)
                
class AddFoodItemIntentHandler(AbstractRequestHandler):
    
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("addFoodItem")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Get slots
        input_slots = handler_input.request_envelope.request.intent.slots
        
        # needed variables
        food_name = input_slots['food_item'].value
        second_food = input_slots['second_item'].value
        third_food = input_slots['third_item'].value
        location = input_slots['drawer'].resolutions.resolutions_per_authority[0].values[0].value.id
        item_qty = input_slots['item_qty'].value
        second_qty = input_slots['second_qty'].value
        third_qty = input_slots['third_qty'].value
        
        # Make lists
        item_list  = [food_name, second_food, third_food]
        qty_list = [item_qty, second_qty, third_qty]
        
        print(item_list)
        print(qty_list)
        
        # Set dictionary
        payload = {'location' : int(location)}
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        new_url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/add_item'
        
        # Loop through 
        for food, qty in zip(item_list, qty_list):
            
            if food == None:
                continue
            else:
                if qty != None:
                    
                    qty  = float(qty)
                    
                payload['name'] = food
                payload['qty'] = qty
                
                print(payload)
                
                r = requests.post(new_url, headers=headers, data=payload)
                
                print('Have got code {} and added {}'.format(r.status_code, food))
        
        added_food = ' and '.join([x for x in item_list if x != None])
        
        speak_output = 'I have added {} to {} '.format(added_food, drawer_map[int(location)])
        
        return handler_input.response_builder.speak(speak_output).response
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                
class DeleteFoodItemIntentHandler(AbstractRequestHandler):
    
    """Handler for Locate Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("deleteFoodItem")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Get slots
        input_slots = handler_input.request_envelope.request.intent.slots
        
        # needed variables
        food_name = input_slots['food_name'].value
        from_location = input_slots['from_location'].resolutions.resolutions_per_authority[0].values[0].value.id
        
        
        new_url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/{}'.format(food_name)
        
        r = requests.get(new_url)
        
        # response
        json_response = r.json()
        
        print('response is {}'.format(json_response))
        
        # selected items 
        selected_food = [x for x in json_response if x.get('location') == int(from_location)]
        
        print(selected_food)
        
        if len(selected_food) == 1:
            
            selected_ = selected_food[0]
            
            print('dict object is of type {} and is {}'.format(type(selected_), selected_))
            
            # Get any existing attributes from the incoming request
            session_attr = handler_input.attributes_manager.session_attributes
            
            session_attr["food_to_delete"] = selected_.get('food_id')
            
            # Define url  
            url = 'https://mammys-freezer-api.herokuapp.com/v1.0/freezer/delete_item/{}'.format(session_attr["food_to_delete"])
            
            # make request
            r = requests.delete(url)
            
            if r.status_code == 200:
                
                session_attr["food_to_delete"] = None
                
            
                speak_output = 'I have removed {} from {}'.format(selected_.get('name'), drawer_map[int(from_location)])
                
            else:
                
                speak_output = 'I encountered a problem as was unable to remove {} please try again'.format(selected_['name'])
                
            return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response) 
        
        elif len(selected_food) == 0:
            
            if len(json_response) > 0:
                
                speak_output = 'I don\'t have it in that location. I have'
                
                # loop through
                for i, item in enumerate(json_response):
                    
                    if i >= 1:
                        
                        speak_output += ' and'
                    
                    speak_output += ' {} in location {}'.format(item.get('name'), drawer_map[int(item.get('location'))])
                    
                speak_output += ' If you  want to remove one of these items, say remove {} from {}'.format(json_response[0].get('name'), drawer_map[int(json_response[0].get('location'))])
                
            else:
                
                speak_output = 'I cannot find the item you requested'
                
            return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response) 
                
                
        else:
            
            # Access session attributes
            # Get any existing attributes from the incoming request
            session_attr = handler_input.attributes_manager.session_attributes
            
            # initiate dictionary
            opt_dict  = {}
            
            for i, val in enumerate(selected_food):
                
                opt_dict[str(i + 1)] = {'name' : val.get('name'), 'i.d.' : val.get('food_id'), 'location' : drawer_map[int(val.get('location'))]}
                
            str_dict = json.dumps(opt_dict)
                
            session_attr["delete_options"] = opt_dict
            
            speak_output = 'This is ambiguous I have too many items. please select an option. '
            
            for options in session_attr["delete_options"].keys():
                
                speak_output += ' option {}, {} in {} with i.d. {}'.format(options, session_attr["delete_options"][options]['name'], session_attr["delete_options"][options]['location'], session_attr["delete_options"][options]['i.d.'])
            
            speak_output += ' please select an option'
            
            reprompt = 'please select an option'

        return (
            handler_input.response_builder.speak(speak_output).ask(reprompt).add_directive(ElicitSlotDirective(
                    updated_intent=Intent(
                        name="selectFoodItem"), 
                    slot_to_elicit="food_option")).response)        


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(LocateFoodIntentHandler())
sb.add_request_handler(checkFoodAgeIntentHandler())
sb.add_request_handler(checkitemIntentHandler())
sb.add_request_handler(MoveFoodItemIntentHandler())
sb.add_request_handler(AddFoodItemIntentHandler())
sb.add_request_handler(DeleteFoodItemIntentHandler())
sb.add_request_handler(UpdateFoodItemIntentHandler())
sb.add_request_handler(SelectFoodIntentHandler())
sb.add_request_handler(checkDrawerContentsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
