import json
from collections import OrderedDict

def flatten_json(json_data, parent_key='', sep='.'):
    items = {}
    for k, v in json_data.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep))
        elif isinstance(v, list) and any(isinstance(item, dict) for item in v):
            for i, item in enumerate(v):
                new_item_key = f"{new_key}{sep}{i}"
                items.update(flatten_json(item, new_item_key, sep))
        else:
            items[new_key] = v
    return items

def nested_json_to_list_of_lists(json_data):
    # Check if the input is a list of JSONs
    if not isinstance(json_data, list):
        json_data = [json_data]

    # Ensure all JSONs have the same keys for consistent headers
    all_keys = set()
    for json_obj in json_data:
        flat_data = flatten_json(json_obj)
        all_keys.update(flat_data.keys())

    headers = list(all_keys)

    data_rows = []
    for json_obj in json_data:
        flat_data = flatten_json(json_obj)
        data_row = [flat_data.get(header) for header in headers]

        # Find the indices of the keys with array objects inside
        array_indices = [headers.index(header) for header in headers if isinstance(flat_data.get(header), list)]

        # If the array_indices are not empty, we need to handle arrays
        if array_indices:
            max_array_len = max(len(flat_data.get(headers[i], [])) for i in array_indices)

            for i in range(max_array_len):
                data_row_copy = data_row.copy()
                for index in array_indices:
                    array_data = flat_data.get(headers[index], [])
                    if i < len(array_data):
                        # Check if the item in the array is a dictionary (nested object)
                        if isinstance(array_data[i], dict):
                            # If it is a dictionary, update the data_row_copy with its values
                            for key, value in array_data[i].items():
                                data_row_copy[index] = key
                                data_row_copy[index + 1] = value
                        else:
                            # If it is not a dictionary, keep the value as it is
                            data_row_copy[index] = array_data[i]
                    else:
                        # If the array has fewer items than the current index, keep the value as None
                        data_row_copy[index] = None
                data_rows.append(data_row_copy)
        else:
            data_rows.append(data_row)

    return [headers, *data_rows]

# Sample list of JSON data with complex nested objects and arrays with nested objects
sample_json_list = '''
[
    {
        "id": 1,
        "name": ["John", "Jane"],
        "address": {
            "city": "New York",
            "country": "USA"
        },
        "contacts": {
            "email": "john@example.com",
            "phone": "123-456-7890"
        },
        "hobbies": [
            {"name": "Reading", "type": "Indoor"},
            {"name": "Hiking", "type": "Outdoor"}
        ]
    },
    {
        "id": 2,
        "name": ["Alice", "Bob"],
        "address": {
            "city": "Los Angeles",
            "country": "USA"
        },
        "contacts": {
            "email": "alice@example.com",
            "phone": "987-654-3210"
        },
        "hobbies": [
            {"name": "Painting", "type": "Indoor"},
            {"name": "Swimming", "type": "Outdoor"}
        ]
    }
]
'''

# Load JSON data into a Python object (list of JSONs)
parsed_json_list = json.loads(sample_json_list)

# Convert the list of complex nested JSONs to a list of lists with headers on the first row
list_of_lists = nested_json_to_list_of_lists(parsed_json_list)





# The variable 'list_of_lists' contains the data in a list of lists format with headers on the first row
for row in list_of_lists:
    print(row)

import json

def list_of_lists_to_json(data_list):
    def parse_value(value):
        try:
            # Attempt to parse the value as JSON
            return json.loads(value.replace("'", '"'))
        except (ValueError, AttributeError):
            # If not a valid JSON or an attribute error (for non-string values), return the value as is
            return value

    def get_nested_key(current_dict, keys):
        for key in keys:
            if key.isdigit():
                key = int(key)
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        return current_dict

    header = data_list[0]
    data_rows = data_list[1:]

    json_data = []

    for row in data_rows:
        row_dict = {}
        for index, value in enumerate(row):
            keys = header[index].split('.')
            current_dict = row_dict
            main_key = keys[0]
            if main_key.isdigit():
                main_key = int(main_key)
            current_dict = get_nested_key(current_dict, [main_key] + keys[1:-1])
            last_key = keys[-1]
            if last_key.isdigit():
                last_key = int(last_key)

            if last_key not in current_dict:
                current_dict[last_key] = parse_value(value)
            else:
                if isinstance(current_dict[last_key], list):
                    current_dict[last_key].append(parse_value(value))
                else:
                    current_dict[last_key] = [current_dict[last_key], parse_value(value)]

        json_data.append(row_dict)

    return json.dumps(json_data, indent=4)

# Example usage:
data = [
    ['hobbies.1.name', 'address.country', 'id', 'contacts.phone', 'hobbies.0.type', 'name', 'hobbies.0.name', 'address.city', 'hobbies.1.type', 'contacts.email'],
    ['Hiking', 'USA', 1, '123-456-7890', 'Indoor', 'John', 'Reading', 'New York', 'Outdoor', 'john@example.com'],
    ['Hiking', 'USA', 1, '123-456-7890', 'Indoor', 'Jane', 'Reading', 'New York', 'Outdoor', 'john@example.com'],
    ['Swimming', 'USA', 2, '987-654-3210', 'Indoor', 'Alice', 'Painting', 'Los Angeles', 'Outdoor', 'alice@example.com'],
    ['Swimming', 'USA', 2, '987-654-3210', 'Indoor', 'Bob', 'Painting', 'Los Angeles', 'Outdoor', 'alice@example.com']
]

json_data = list_of_lists_to_json(list_of_lists)
print(json_data)


