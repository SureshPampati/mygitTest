def nested_json_to_list_of_lists(data, keys=None):
    if keys is None:
        keys = []

    if isinstance(data, dict):
        # If the data is a dictionary, recursively call the function for each key-value pair
        for key, value in data.items():
            nested_json_to_list_of_lists(value, keys + [key])
    else:
        # If the data is not a dictionary, we've reached a leaf node, so add it to the list of lists
        list_of_lists.append(keys + [data])


# Example nested JSON object
nested_json = {
    "person1": {
        "name": "Alice",
        "age": 30,
        "address": {
            "city": "New York",
            "country": "USA"
        }
    },
    "person2": {
        "name": "Bob",
        "age": 25,
        "address": {
            "city": "San Francisco",
            "country": "USA"
        }
    }
}

# Initialize the list of lists
list_of_lists = []


# Convert nested JSON to list of lists
nested_json_to_list_of_lists(nested_json)
print(list_of_lists)
# Print the result
for row in list_of_lists:
    print(row)
