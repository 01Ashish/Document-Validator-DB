import json
import re

def rename_degree_key(data):
    try:
        data["documentInfo"][0]["providerName"] = data["documentInfo"][0].pop("name")
    except:
        data
    return json.dumps(data,indent=4)


def camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def convert_keys_to_camel_case(obj):
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = camel_case(k.lower()) 
            new_dict[new_key] = convert_keys_to_camel_case(v)
        return new_dict
    elif isinstance(obj, list):
        return [convert_keys_to_camel_case(item) for item in obj]
    else:
        return obj
    
def regex_search(var):
    text = str(var)
    start_index = text.find('{')

    # Find the ending index of the last }
    end_index = text.rfind('}')

    # Extract the desired content
    clean_text = text[start_index:end_index + 1]
    data = json.loads(clean_text)
    return data
 