import requests

parameters = {
    "amount": 10,
    "type:": "boolean"
    }

question_response = requests.get(
    url="https://opentdb.com/api.php?amount=10&type=boolean",
    params=parameters)
question_response.raise_for_status()
question_data = question_response.json()["results"]
print(question_data)
