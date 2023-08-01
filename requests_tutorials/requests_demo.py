import requests
url = 'https://jsonplaceholder.typicode.com/posts/'

# adding a payload
payload = {'id':[1,2], 'userId':1}

# get requests allows to retrieve data
response = requests.get(url,params=payload)
response1 = requests.head(url)
print(response.text)

print(response.json())

print(response.status_code)



# post allows to create new data

# define new data to create

new_data = {
    "userID": 1,
    "id": 1,
    "title": "Making a POST request",
    "body": "This is the data we created"
}

url_post = "https://jsonplaceholder.typicode.com/posts"

post_response = requests.post(url_post, new_data)

print(post_response.json())

