
The given directory AirVisual_API has a python file “TestAPIs.py”

Requirements: 

Create a few API tests that will cover the following scenarios: 

a)	Api authorisation (403 if no auth token, 200 if correct provided) - for any api can be used – Test case 1& 2
b)	Check api : api.airvisual.com/v2/states?country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}  will return the 6 states of Australia and validate names – Test case 3

c)	Use certain api to find the nearest city data – Test case 4 

d)	Use the longitude and latitude get the temperature form the nearest city and validate the return Json is in the correct format as specified in the documentation - Test case 4

Prerequisite

The executor of this python script should have python installed with 3.x version.
From the command prompt 

pip install requests
pip show requests

python TestAPIs.py 

Attached a sample screen shot of my run 

