from tkinter import *
from PIL import ImageTk, Image
import requests
import json

#TODO
#may need to login manually to make it work again



root = Tk()
root.title('Snir\'s Weather APP')
#root.iconbitmap('c:/X/X')
root.geometry("600x100")
#root.configure(background='green')

#Refference for API
# https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=37061&distance=25&API_KEY=2EB1E9BC-4264-41C0-A814-A1EE3F29EEDB
# Your API Key: 2EB1E9BC-4264-41C0-A814-A1EE3F29EEDB

#Create ZIP Lookup Function
def zipLookup():
    # zip.get()
    # zipLabel = Label(root, text=zip.get())
    # zipLabel.grid(row=1, column=0, columnspan=2)

    try:

        api_request = requests.get(
            "https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + zip.get() + "&distance=25&API_KEY=2EB1E9BC-4264-41C0-A814-A1EE3F29EEDB")
        api = json.loads(api_request.content)

        city = api[0]['ReportingArea']
        quality = api[0]['AQI']
        category = api[0]['Category']['Name']

        if category == "Good":
            weather_color = "#0C0"
        elif category == "Moderate":
            weather_color = "#FFFF00"
        elif category == "Unhealthy for Sensitive Groups":
            weather_color = "#ff9900"
        elif category == "Unhealthy":
            weather_color = "#FF0000"
        elif category == "Very Unhealthy":
            weather_color = "#990066"
        elif category == "Hazardous":
            weather_color = "#660000"

        root.configure(background=weather_color)

        myLabel = Label(root, text=city + " Air Quality " + str(quality) + " " + str(category), font=("Helvetica", 0),
                        background='green')
        myLabel.grid(row=1, column=0, columnspan=2)
    except Exception as e:
        api = "Error..."

try:
    api_request = requests.get(
        "https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=37061&distance=25&API_KEY=2EB1E9BC-4264-41C0-A814-A1EE3F29EEDB")
    api = json.loads(api_request.content)

    city = api[0]['ReportingArea']
    quality = api[0]['AQI']
    category = api[0]['Category']['Name']

    if category == "Good":
        weather_color = "#0C0"
    elif category == "Moderate":
        weather_color = "#FFFF00"
    elif category == "Unhealthy for Sensitive Groups":
        weather_color = "#ff9900"
    elif category == "Unhealthy":
        weather_color = "#FF0000"
    elif category == "Very Unhealthy":
        weather_color = "#990066"
    elif category == "Hazardous":
        weather_color = "#660000"

    root.configure(background=weather_color)

    myLabel = Label(root, text=city + " Air Quality " + str(quality) + " " + str(category), font=("Helvetica", 0), background='green')
    myLabel.grid(row=1, column=0, columnspan=2)
except Exception as e:
    api = "Error..."

zip = Entry(root)
zip.grid(row=0, column=0, sticky=W+E+N+S)

zipButton = Button(root, text="LookUp Zipcode", command=zipLookup)
zipButton.grid(row=0, column=1)

# print(api)
# print(api_request)



root.mainloop()