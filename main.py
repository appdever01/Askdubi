from flask import Flask,request
from dotenv import load_dotenv
import os
from car_info import get_car_brands, get_car_models, get_car_years, get_car_addresses, get_car_results
from wa_function import *

load_dotenv()
app = Flask(__name__)

user_track = {}
brands = get_car_brands()
# Main logic to handle user interaction
def handle_user_input(phone_number, message, btn_id):
    if btn_id == "go_back":
            user_track[phone_number]['step'] = 'start'
            del user_track[phone_number]['brandIndex'] 
            handle_user_input(phone_number, "start", "")
    elif btn_id == "go_back_model":
        user_track[phone_number]['step'] = 'choose_brand'
        handle_user_input(phone_number, "choose_brand", "")
        
    step = (user_track[phone_number]['step']) 
    if step == 'start':
        # Step 1: Show car brands as a numbered list
        if brands:
            brand_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(brands.values())])
            send_message(phone_number, f"*Please choose a car brand by replying with the corresponding number:*\n\n{brand_list}\n")
            user_track[phone_number]['step'] = 'choose_brand'  # Update user's step in the conversation
            user_track[phone_number]['brands'] = brands  # Save brands to reference later
        else:
            send_message(phone_number, "Sorry, unable to fetch car brands.")

    elif step == 'choose_brand':
        # Step 2: User selects a car brand by replying with a number
        if message !='':
            try:
                chosen_brand_index = user_track.get(phone_number, {}).get('brandIndex') if user_track.get(phone_number, {}).get('brandIndex')  else int(message) - 1  # Convert user input to an index
                print(chosen_brand_index)
                user_track[phone_number]['brands'] = brands
                brand_ids = list(brands.keys())
                options = [
                            {"id": "go_back", "title": "Go Back"}
                        ]
                if 0 <= chosen_brand_index < len(brand_ids):
                    brand_id = brand_ids[chosen_brand_index]
                    user_track[phone_number]['brand'] = brand_id  # Save selected brand
                    user_track[phone_number]['brandIndex'] = chosen_brand_index  # Save selected brand index
                    send_message(phone_number, f"_*Fetching {brands[brand_id]} models... please wait*_ ⏳🚗")
                    models = get_car_models(brand_id)
                    if models:
                        model_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(models.values())])
                        send_btn_msg(phone_number, f"*Please choose a car model by replying with the corresponding number:*\n\n{model_list}\n", options)
                        user_track[phone_number]['step'] = 'choose_model'
                        user_track[phone_number]['models'] = models  
                    else:
                        send_btn_msg(phone_number, f"Sorry, no models available for the selected brand.", options)
                        user_track[phone_number]['step'] = 'choose_brand' 
                else:
                    send_message(phone_number, "Invalid selection ❗️. Please reply with a valid number. ")
            except ValueError:
                send_message(phone_number, "Invalid input ❗️. Please reply with a number corresponding to your choice.")

    elif step == 'choose_model':
        # Step 3: User selects a car model by replying with a number
        if message == "":
            user_track[phone_number]['step'] = 'choose_model'
            del user_track[phone_number]['brandIndex'] 
            handle_user_input(phone_number, "", "")
        else:
            try:
                chosen_model_index = int(message) - 1  # Convert user input to an index
                models = user_track[phone_number]['models']
                model_ids = list(models.keys())
                options = [
                            {"id": "go_back_model", "title": "Go Back"}
                        ]
                if 0 <= chosen_model_index < len(model_ids):
                    model_id = model_ids[chosen_model_index]
                    user_track[phone_number]['model'] = model_id  # Save selected model
                    user_track[phone_number]['step'] = 'choose_year'
                    brand_id = user_track[phone_number]['brand']
                    years = get_car_years(model_id,brand_id)
                    
                    if years:
                        year_list = "\n".join([f"{i+1}. {year}" for i, year in enumerate(years)])
                        
                        send_btn_msg(phone_number, f"*Please choose your prefered car year by replying with the corresponding number:*\n\n{year_list}\n", options)
                        user_track[phone_number]['step'] = 'choose_year'
                        user_track[phone_number]['years'] = years  
                    else:
                        send_btn_msg(phone_number, "Sorry, no car is available for the selected model.", options)
                        user_track[phone_number]['step'] = 'choose_model' 
                else:
                    send_message(phone_number, "Invalid selection  ❗️. Please reply with a valid number. ")
            except ValueError:
                send_message(phone_number, "Invalid input ❗️. Please reply with a number corresponding to your choice.")

    elif step == 'choose_area':
        try:
            brand_id = user_track[phone_number]['brand']
            model_id = user_track[phone_number]['model']
            year = user_track[phone_number]['year']
            print(brand_id)
            print(model_id)
            print(year)
            addresses = get_car_addresses(model_id,brand_id,year)
            
            if addresses:
                addresses_list = "\n".join([f"{i+1}. {address}" for i, address in enumerate(addresses)])
                send_message(phone_number, f"*Please choose your preferred car address by replying with the corresponding number:*\n\n{addresses_list}\n")
                user_track[phone_number]['step'] = 'final_options_area'
                user_track[phone_number]['addresses'] = addresses  
            else:
                send_message(phone_number, "Sorry, no car is available for the selected model and year.")
                user_track[phone_number]['step'] = 'choose_area' 
        except ValueError:
            send_message(phone_number, "Invalid input ❗️. Please reply with a number corresponding to your choice.")


    elif step == 'choose_year':
        # Step 4: User inputs a year
        try:
            chosen_year_index = int(message) - 1  # Convert user input to an index
            years = user_track[phone_number]['years'] 
            
            if 0 <= chosen_year_index < len(years):
                year = years[chosen_year_index]
                user_track[phone_number]['year'] = year 
                options = [
                    {"id": "show_result", "title": "Show Results"},
                    {"id": "choose_area", "title": "Choose Area"},
                    {"id": "go_back", "title": "Start Again"}
                ]
                
                send_btn_msg(phone_number, "What would you like to do next? 🤔", options)
                user_track[phone_number]['step'] = 'final_options'
                
            else:
                send_message(phone_number, "Invalid selection  ❗️. Please reply with a valid number.")
        
        except ValueError:
            send_message(phone_number, "Invalid input ❗️. Please reply with a number corresponding to your choice.")
            
    elif step == 'final_options_area':
        try:
            chosen_address_index = int(message) - 1  # Convert user input to an index
            addresses = user_track[phone_number]['addresses'] 
            
            if 0 <= chosen_address_index < len(addresses):
                address = addresses[chosen_address_index]
                user_track[phone_number]['address'] = address 
              
                send_message(phone_number, "_*Fetching car information... please wait*_ ⏳🚗")
                brand_id = user_track[phone_number]['brand']
                model_id =  user_track[phone_number]['model']
                year =  user_track[phone_number]['year']
                results = get_car_results(brand_id, model_id,year)
                if results:
                    for result in results:
                        print(result['image'])
                        message = f"""*{result['name']}*\n\n*Condition:* {result['mw_condition']}\n*Year:* {result['mw_year']}\n*Price:* {result['mw_price']}\n*Transmission:* {result['mw_transmission']}\n*Fuel Type:* {result['mw_fueltype']}\n*Engine Size:* {result['mw_enginesize']}\n*Address:* {result['mw_street_addr']}\n\nVisit {result['link']} for full details ✨🚗."""
                        send_image(phone_number, result['image'],  message)
                       
                else:
                    send_message(phone_number, "No cars found for the selected model and year.")
                user_track[phone_number]['step'] = 'start'
                
            else:
                send_message(phone_number, "Invalid selection  ❗️. Please reply with a valid number.")
        
        except ValueError:
            send_message(phone_number, "Invalid input ❗️. Please reply with a number corresponding to your choice.")
            
        
    elif step == 'final_options':
        # Step 5: Final options
        try:
            option = btn_id
            if option == 'show_result':
                send_message(phone_number, "_*Fetching car information... please wait*_ ⏳🚗")
                brand_id = user_track[phone_number]['brand']
                model_id =  user_track[phone_number]['model']
                year =  user_track[phone_number]['year']
                results = get_car_results(brand_id, model_id,year)
                if results:
                    for result in results:
                        print(result['image'])
                        message = f"""*{result['name']}*\n\n*Condition:* {result['mw_condition']}\n*Year:* {result['mw_year']}\n*Price:* {result['mw_price']}\n*Transmission:* {result['mw_transmission']}\n*Fuel Type:* {result['mw_fueltype']}\n*Engine Size:* {result['mw_enginesize']}\n*Address:* {result['mw_street_addr']}\n\nVisit {result['link']} for full details ✨🚗."""
                        send_image(phone_number, result['image'],  message)
                else:
                    send_message(phone_number, "No cars found for the selected model and year.")
                    
                user_track[phone_number]['step'] = 'start'
            elif option == "choose_area":
                user_track[phone_number]['step'] = 'choose_area'
                handle_user_input(phone_number, "choose_area","")
            elif option == "go_back":
                user_track[phone_number]['step'] = 'start'
                handle_user_input(phone_number, "start","")
            else:
                send_message(phone_number, "Invalid selection. Please choose 'Show Results', 'Choose Area, or 'Start Again'.")
        except ValueError:
            send_message(phone_number, "Invalid input. Please choose 'Show Results', 'Choose Area, or 'Start Again'.")
            
@app.route('/', methods=['POST'])
def receive_posted_data():
    webhook_data = request.json
    if  webhook_data['msg'] != '' or webhook_data['btn_id'] != '':
        if webhook_data['to'] not in user_track:
            user_track[webhook_data['to']] = {}
        if 'step' not in user_track[webhook_data['to']]:
            user_track[webhook_data['to']]['step'] = 'start'
        handle_user_input(webhook_data['to'], webhook_data['msg'],webhook_data['btn_id'])
    print(webhook_data)
    return '', 200


         
@app.route('/webhook', methods=['POST'])
def webhook_post():
    body = request.json
    if body.get('object'):
        entry = body.get('entry', [])[0]
        changes = entry.get('changes', [])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])

        
        if messages:
            message = messages[0]
            wam_id = message.get('id')
            username = value.get('contacts', [])[0].get('profile', {}).get('name')
            btn_id = ''
            msg_body = ''
            msg_type = message.get('type')

            if msg_type == 'interactive':
                btn_id = message.get('interactive', {}).get('button_reply', {}).get('id')
            elif msg_type == 'text':
                msg_body = message.get('text', {}).get('body')

            phone_number_id = value.get('metadata', {}).get('phone_number_id')
            display_phone_number = value.get('metadata', {}).get('display_phone_number')
            from_number = message.get('from')
            refined_json = {
                "id": phone_number_id,
                "username": username,
                "wam_id": wam_id,
                "phone_number": display_phone_number,
                "msg": msg_body,
                "to": from_number,
                "type": msg_type,
                "btn_id": btn_id
            }
            requests.post('https://6bbf-102-89-75-4.ngrok-free.app', json=refined_json)
            return '', 200
        else:
            return '', 404 
        
@app.route('/webhook', methods=['GET'])
def webhook_get():
    verify_token = os.getenv("VERIFY_TOKEN")

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            return '', 403



if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 1337)), debug=True)