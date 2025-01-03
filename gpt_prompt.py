import base64
import json
import requests
import os
from prompts_to_json import regex_search,convert_keys_to_camel_case,rename_degree_key
from dotenv import load_dotenv
from prompt import board_certificate_prompt, dea_prompt, pli_prompt, ofac_prompt, sam_prompt, medicare_opt_out_prompt, oig_prompt, npi_prompt, caqh_prompt 


load_dotenv()
api_key = os.getenv("api_key")

def process_image_first(image_path,user_input):
    
    
    if user_input["document_name"] == "npi":
        prompt = npi_prompt
    elif user_input["document_name"] == "caqh":
        prompt = caqh_prompt
    elif user_input["document_name"] == "dea":
        prompt = dea_prompt
    elif user_input["document_name"] == "professional_license":
        prompt = pli_prompt
    elif user_input["document_name"] == "ofac":
        prompt = ofac_prompt
    elif user_input["document_name"] == "sam":
        prompt = sam_prompt
    elif user_input["document_name"] == "medicare_opt_out":
        prompt = medicare_opt_out_prompt
    elif user_input["document_name"] == "oig":
        prompt = oig_prompt
    elif user_input["document_name"] == "board_certificate":
        prompt = board_certificate_prompt
    
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-turbo",
    "messages": [
        {
            "role" : "system",
            "content" : prompt
        },
        {
        "role": "user",
        "content": [            
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            },
            f"Provided JSON Data to validate - {user_input}"
        ]
        }
    ],
    "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
     # Check for response status and handle errors
    if response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return {"error": "API request failed", "details": response.text}

    # Try to parse the response, with error handling
    try:
        data = response.json()
        if "choices" in data:
            # Access the content safely
            var = data['choices'][0]['message']['content']
            print(var)
        else:
            print("Unexpected response format:", data)
            return {"error": "Unexpected response format", "details": data}
    except Exception as e:
        print("Error parsing JSON response:", e)
        return {"error": "JSON parsing error", "details": str(e)}
    # print(var)
    # board_name,line_of_business,license_number,issue_date, issued_to = regex_search_pli(var)
    # print("***************")
    # print(board_name,line_of_business,license_number,issue_date, issued_to)
    # return board_name,line_of_business,license_number,issue_date, issued_to
    try:
        result =  regex_search(var)
    except:
        result = var
    converted_data = convert_keys_to_camel_case(result)
    # if len(converted_data["documentInfo"][0].keys())>1:
    #     print(len(converted_data["documentInfo"][0].keys()))
    #     converted_data["documentInfo"][0]["validationType"]='yes'
    # else:
    #     converted_data
    return converted_data

