# IMPORTING LIBRARIES
import requests
import datetime as dt
import os

# CONSTANTS
# PERSONAL DETAILS
GENDER = os.environ.get("GENDER")
WEIGHT = os.environ.get("WEIGHT")
HEIGHT = os.environ.get("HEIGHT")
AGE = os.environ.get("AGE")

# NUTRIONIX
NUTRIONIX_APP_ID = os.environ.get("NUTRIONIX_APP_ID")
NUTRIONIX_APP_KEY = os.environ.get("NUTRIONIX_APP_KEY")
NUTRIONIX_API_END_POINT = os.environ.get("NUTRIONIX_API_END_POINT")
NUTRIONIX_USER_ID = "0"

# SHEETY
SHEETY_API_ENDPOINT = os.environ.get("SHEETY_API_ENDPOINT")
SHEETY_AUTHORIZATION = os.environ.get("SHEETY_AUTHORIZATION")

nutrionix_header = {
    "x-app-id": NUTRIONIX_APP_ID,
    "x-app-key": NUTRIONIX_APP_KEY,
    "x-remote-user-id": NUTRIONIX_USER_ID,
}

user_prompt = """Welcome to Exercise Tracker.
Please enter the exercises you did with the duration of each exercise:
(Eg: ran for 5 miles and walked for 10 miles.)
User Input: """
user_response = input(user_prompt)

nutrionix_params = {
    "query": user_response,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

nutrionix_response = requests.post(
    url=NUTRIONIX_API_END_POINT, headers=nutrionix_header, json=nutrionix_params
)
exercise_data = nutrionix_response.json()["exercises"]

date = dt.datetime.now().strftime("%d/%m/%Y")
time = dt.datetime.now().strftime("%X")
sheety_header = {"Authorization": SHEETY_AUTHORIZATION}

for exercise in exercise_data:
    exercise_name = exercise["name"].title()
    calories = exercise["nf_calories"]
    duration = exercise["duration_min"]

    sheety_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise_name,
            "duration": duration,
            "calories": calories,
        }
    }

    sheety_response = requests.post(
        url=SHEETY_API_ENDPOINT, headers=sheety_header, json=sheety_params
    )
    print(sheety_response.text)

print("Exiting...")
