import requests
import json
import os

def sendRequest(json_data):
    url = 'http://localhost:5000/path'  # The API endpoint

    # Log the JSON being sent
    print('\nSending JSON:', json_data)

    try:
        response = requests.post(url, json=json_data, headers={'Content-Type': 'application/json'})

        # Log the response to the console
        print('\nResponse:', response.json())

        # Create a file and write the response data to it
        with open('response.json', 'w', encoding='utf8') as f:
            json.dump(response.json(), f, indent=2, ensure_ascii=False)
        print('\nResponse data has been written to response.json')

        return response.json()

    except requests.exceptions.RequestException as error:
        print('Error:', error)

# Example usage of the send_request function
data = {
    "obstacles": [
        {"x": 10, "y": 10, "d": 0, "id": 1},
        {"x": 8, "y": 8, "d": 2, "id": 5},
        {"x": 10, "y": 12, "d": 4, "id": 7},
        {"x": 17, "y": 1, "d": 6, "id": 2}
    ],
    "robot_x": 1,
    "robot_y": 1,
    "robot_dir": 0,
    "retrying": False
}

# Call the function with the JSON data
# sendRequest(data)

# d-values for obstacles:
# up : 0
# right : 2
# down : 4
# left : 6
