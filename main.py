import requests

response = requests.get("https://api.open-meteo.com/v1/forecast", params={
    "latitude": 44.43,
    "longitude": 26.10,
    "current_weather": True
})

data = response.json()["current_weather"]
print(f"Bucharest: {data['temperature']}°C, wind {data['windspeed']} km/h")
