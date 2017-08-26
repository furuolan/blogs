import datetime
import os
import requests

def get_location(address):
    """
    http://maps.googleapis.com/maps/api/geocode/json?address=San%20Francisco,+CA&sensor=false
    """
    params = {"address": address, "sensor": "false"}
    resp = requests.get("http://maps.googleapis.com/maps/api/geocode/json", 
        params=params)
    resp = resp.json()
    lat = resp["results"][0]["geometry"]["location"]["lat"]
    lng = resp["results"][0]["geometry"]["location"]["lng"]
    return {"lat": lat, "lng": lng}

def get_timezone(location, timestamp):
    """
    https://maps.googleapis.com/maps/api/timezone/json?location=37.77492950,-122.41941550&timestamp=1331161200&sensor=false
    """
    params = {"location": str(location["lat"]) + "," + str(location["lng"]), 
        "timestamp": timestamp, "sensor": "false"}
    resp = requests.get("https://maps.googleapis.com/maps/api/timezone/json", 
        params=params)
    resp = resp.json()
    lat = resp["dstOffset"]
    lng = resp["rawOffset"]
    return {"dstOffset": lat, "rawOffset": lng}

def current_utc_diff():
    now = datetime.datetime.utcnow()
    start = datetime.datetime(1970, 1, 1)
    return (now - start).total_seconds()

def city_time(city):
    location = get_location(address=city)
    timestamp = current_utc_diff()
    google_timezone = get_timezone(location=location, timestamp=timestamp)
    dst_offset = google_timezone["dstOffset"]
    raw_offset = google_timezone["rawOffset"]
    current_time = datetime.datetime.fromtimestamp(
            timestamp + raw_offset + dst_offset)
    return current_time

if __name__ == "__main__":
    print(city_time("San Francisco"))
