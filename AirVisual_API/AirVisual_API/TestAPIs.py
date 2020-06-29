import requests
import jsonschema

url = "http://api.airvisual.com/"
payload = {}
headers= {'Content-Type':'application/json'}
apiKey = "d9c8422b-03d4-4571-b389-02477a01647f"
invalidApiKey = "abcde"
success_status = 200
forbidden_status = 403
internal_server_error_status = 500
coordinates = []

def validateValidAuth():
    try:
        url_string = url + "v2/countries?"
        params = {'key': apiKey}
        response = requests.get(url_string, params)
        # print(response.text)
        assert response.status_code == success_status
        print("Test 1 (test valid auth): Status " + str(response.status_code))
    except AssertionError as e:
        print("validateValidAuth assertion error")

def validateInvalidAuth():
    try:
        url_string = url + "v2/countries?"
        params = {'key': invalidApiKey}
        response = requests.get(url_string, params)
        # print(response.text)
        assert response.status_code == forbidden_status
        print("Test 2 (test invalid auth): Status " + str(response.status_code))
    except AssertionError as e:
        print("validateInvalidAuth assertion error")

def listStatesAPI():
    try:
        country = "Australia"
        au_states = ['New South Wales', 'Queensland', 'South Australia', 'Tasmania', 'Victoria', 'Western Australia']
        url_string = url + "v2/states?country=" +country+ "&key="+apiKey
        response = requests.request("GET", url_string, headers=headers, data = payload)
        # print(response.text)
        assert response.status_code == success_status
        response_body = response.json()
        resp_states = [str(i['state']) for i in response_body["data"]]
        print("Test 3 (list states): Status " + str(response.status_code))
        print("{} : {}".format(country, str(resp_states)))
        assert au_states == resp_states
    except AssertionError as e:
        print("listStatesAPI assertion error")

def nearestCityDataAPI():
    try:
        global coordinates
        url_string = url + "v2/nearest_city?key="+apiKey
        response = requests.request("GET", url_string, headers=headers, data = payload)
        assert response.status_code == success_status
        response_body = response.json()
        print("Test 4 (nearestCityData): Status " + str(response.status_code))
        print("{}".format(str(response_body["data"])))
        coordinates = str(response_body["data"]["location"]["coordinates"])
    except AssertionError as e:
        print("nearestCityDataAPI assertion error")

def getCityTemperatureAPI():
    try:
#         latitude, longitude = "-37.987461", "145.214859"
        latitude, longitude = str(coordinates[0]), str(coordinates[1])
        url_string = url + "v2/nearest_city?lat="+latitude+"&lon="+longitude+"&key="+apiKey
        response = requests.request("GET", url_string, headers=headers, data = payload)
        assert response.status_code == success_status
        response_body = response.json()
        # print(jsonschema.validate(instance=response_body, schema=json_schema))
        print("Test 5 (getCityTemperature): Status " + str(response.status_code))
        print("{}: {}".format(str(response_body["data"]["city"]), 
                              str(response_body["data"]["current"]["weather"]["tp"])))

    except AssertionError as e:
        print("getCityTemperatureAPI assertion error")

if __name__ == "__main__":
    validateValidAuth()
    validateInvalidAuth()
    listStatesAPI()
    nearestCityDataAPI()
    getCityTemperatureAPI()

    """
    To enable for CI/CD (Bamboo):
    Run ./docker_run.sh
    """