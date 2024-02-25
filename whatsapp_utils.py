import json
import requests
import re

def log_http_response(response):
    '''
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")
    '''


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def get_product_list(recipient,product_data):
    curl_data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "interactive",
        "interactive": {
            "type": "product_list",
            "header": {
                "type": "text",
                "text": "Most Popular"
            },
            "body": {
                "text": "Here are our hottest dishes this week⬇"
            },
            "action": {
                "catalog_id": "916625162965361",
                "sections": []
            }
        }
    }

    for title, product_items in product_data.items():
        section = {
            "title": title,
            "product_items": [{"product_retailer_id": pid} for pid in product_items]
        }
        curl_data["interactive"]["action"]["sections"].append(section)

    return json.dumps(curl_data, indent=2)

def get_menu_shortcuts(recipient,options,res_name):
    try:
        curl_data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": f"Welcome to {res_name}"
                },
                "body": {
                    "text": "Choose one of our Menu Shortcuts to start exploring",
                },
                "action": {
                    "button": "Shortcuts",
                    "sections": [
                        {
                            "title": "Categories",
                            "rows": [],
                        },
                    ],
                },
            }
        }

        for index, option in enumerate(options):
            row = {
                "id": str(index),
                "title": option,
                "description": options[option],
            }
            curl_data["interactive"]["action"]["sections"][0]["rows"].append(row)
    except Exception as e:
        print("Error:",e)
    return json.dumps(curl_data, indent=2)


def get_interactive_input(recipient,button_list,res_name):
    """
    "type": "IMAGE",
                "image": {
                    "id": "1471377563734275"
                }
    """
    curl_data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {
                "type": "text",
                "text": f"Welcome to {res_name}"
            },
            "body": {
                "text": f"Welcome to {res_name} I'm your personal assistant and will help your order food!\nPlease explore our one of the options"
            },
            "action": {
                "buttons": []
            }
        }
    }

    for index, button_text in enumerate(button_list):
        button = {
            "type": "reply",
            "reply": {
                "id": str(index),
                "title": button_text,
            }
        }
        curl_data["interactive"]["action"]["buttons"].append(button)

    return json.dumps(curl_data, indent=1)
'''
async def send_message(data):
    ACCESS_TOKEN = "EAAE9WW4QS7IBO2Hc4H8yMLZADkIxxxNaOWLDR64rjdMia4BOIwTHhL1hwyspgiL4ix2ZBJrb0wEPep0wvUgbCkXoZBqf4aP0HxBZBM6mN7m98lgHzZC3luRUEG2fW6kgCaZBUfdVV9ZCxZAfWJrxJsSR3AuRWZAPnxwgf0ZAP9tNxOV0ol3PwtBSFhdtGUdG3EiXnInTSOaoPC4ZAVzmjDe"
    VERSION = "v18.0"
    PHONE_NUMBER_ID = "223988317457113"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = "https://graph.facebook.com" + f"/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    #print("Status:", response.status)
                    #print("Content-type:", response.headers["content-type"])

                    html = await response.text()
                    #print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))

'''
def send_message(data):
    ACCESS_TOKEN="EABlasXlfRHIBO5rk4udfml165sdfD0TZA9CX1Spr0lmUsTWTA253ZAXW4yZCU4KlrMDYC8wfNZCiJpgVVEFNsrfoPDTJVTHlyCB2ZA81f0yyD78wIr4sJ9S5Mm8tvN7eWr4qgRQ8yX4UWWm0VBfht15xS1NHDJ9vjKAeAuJBZCD5LmW3F5jovZC0lYlSgIu2L8MacGWJz15OKloep4ZD"
    VERSION="v18.0"
    PHONE_NUMBER_ID= "238523389341337"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    print(data)
    try:
        response = requests.post(url, data=data, headers=headers, timeout=3)  # 20 seconds timeout as an example
    except Exception as e:
        print(e)
    print("Done")


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)
    #print(whatsapp_style_text)
    return whatsapp_style_text


def process_whatsapp_message(body):
    try:
        #print("contactsssss",body["entry"][0]["changes"][0]["value"]["contacts"][0])
        wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
        name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
        phone_number_id = body["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
        # print(phone_number_id)
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        message_type = message["type"]
        from_number = message["from"]
    except:
        data = {
            "statusCode": 200,
            "body": "OK"
        }
        return json.dumps(data)
    #print(message)
    #print("Messaaaaaaaggggeee",message)
    #print(message_type)
    try:
        if(message_type=="text"):
            message_body = message["text"]["body"]
            #response = generate_response(message_body)
            if("menu" in message_body.lower()):
                button_list = ["What's Popular", "Menu Categories", "Preferences/Search"]
                res_name="Muraamba"
                curl = get_interactive_input(recipient=from_number, button_list=button_list,
                                                        res_name=res_name)
                #print(curl_expression)
            else:
                curl = get_text_message_input(recipient=from_number, text=f"Hey, we are updating. Thanks for connecting {name}")
                #print("Curllll",curl)

        elif(message_type=="interactive"):
            if (message["interactive"]["type"]=="button_reply"):
                title=message["interactive"]["button_reply"]["title"]
                #print("Titleeeeeeeeee", title)
                if("menu categories" in title.lower()):
                    options = {
                        "All Day Menu": "Complete Meals",
                        "Thalis": "U know what",
                        "Sweets": "Deserts"
                    }
                    curl = get_menu_shortcuts(recipient=from_number,options=options,res_name="Muraamba")
                elif("preference" in title.lower()):
                    curl=get_text_message_input(recipient=from_number,text="feature/Coming soon")
                elif("menu" in title.lower()):
                    button_list = ["What's Popular", "Menu Categories", "Preferences/Search"]
                    res_name = "Muraamba"
                    curl = get_interactive_input(recipient=from_number, button_list=button_list,res_name=res_name)
                elif("what's popular" in title.lower()):
                    product_data = {
                        "Bestsellers": ["39", "12", "15", "30", "16"],
                        "Best Rated": ["39", "13"]
                    }
                    curl = get_product_list(recipient=from_number, product_data=product_data)
                else:
                    button_list = ["What's Popular", "Menu Categories", "Preferences/Search"]
                    res_name = "Muraamba"
                    curl = get_interactive_input(recipient=from_number, button_list=button_list,
                                                            res_name=res_name)
            elif(message["interactive"]["type"]=="list_reply"):
                title = message["interactive"]["list_reply"]["title"]
                if(title=="All Day Menu"):
                    product_data = {
                        "Bestsellers": ["39", "12", "15", "30", "16"],
                        "Best Rated": ["39", "13"]
                    }
                    curl = get_product_list(recipient=from_number,
                                                       product_data=product_data)
                    '''
                    curl = get_text_message_input(recipient=from_number,
                                                  text=f"Hey {name}, {title} will be available soon.")
                    '''
                else:
                    curl = get_text_message_input(recipient=from_number,
                                                  text=f"Hey {name}, {title} will be available soon.")
    except Exception as e:
        print("Error: ",e)
    send_message(curl)

def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
