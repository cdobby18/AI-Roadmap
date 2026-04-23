import requests


def get_age_prediction(name):
    
    url = "https://api.agify.io"

    params = {
        "name": name
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        print("API RESPONSE")
        print("-----------------------")
        print("Name:", data["name"])
        print("Predicted Age:", data["age"])
        print("Sample Size:", data["count"])

    else:
        print("Error:", response.status_code)


def main():

    name = input("Enter a name: ")

    get_age_prediction(name)


main()