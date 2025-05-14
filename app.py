from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import random
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

with open("places.json", "r", encoding="utf-8") as file:
    places = json.load(file)

def get_random_place():
    return random.choice(places)

def get_place_by_index(index):
    if 0 <= index < len(places):
        return places[index]
    return get_random_place()

def check_guess(guess, actual_coords):
    geolocator = Nominatim(user_agent="geoGame")
    try:
        location = geolocator.geocode(guess)
        if location is None:
            return "Location not found.", None
        user_coords = (location.latitude, location.longitude)
        distance = geodesic(user_coords, tuple(actual_coords)).km
        if distance < 50:
            message = "Wow nailed it +100 points"
        elif distance < 300:
            message = "Nice you're pretty close +70 points"
        elif distance < 1000:
            message = "Not bad not great +40 points"
        else:
            message = "Yeah not even close +10 points"
        return message, round(distance)
    except Exception:
        return "Something went wrong.", None

@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def play(request: Request):
    if request.method == "POST":
        form = await request.form()
        guess = form.get("guess", "")
        place_idx = int(form.get("place_idx", "0"))
        spot = get_place_by_index(place_idx)
        message, distance = check_guess(guess, spot["coords"])
        new_spot = get_random_place()
        html = f"""
        <!DOCTYPE html>
        <html><head><title>Dummed Down GeoGuessr</title><link rel='stylesheet' href='/static/style.css'></head><body>
        <div class='container'><h1>Dummed Down GeoGuessr</h1>
        <div id='game-area'>
        <div id='result'>{message}{' (' + str(distance) + ' km from ' + spot['name'] + ')' if distance is not None and message != 'Location not found.' else ''}</div>
        <img src='{new_spot['img']}' alt='Place Image' width='400'>
        <div id='hint'>Hint: {new_spot['hint']}</div>
        <form action='' method='post'>
            <input type='hidden' name='place_idx' value='{places.index(new_spot)}'>
            <input type='text' name='guess' placeholder='Guess the location'>
            <input type='submit' value='Guess'>
        </form></div></div></body></html>
        """
        return HTMLResponse(html)
    else:
        spot = get_random_place()
        html = f"""
        <!DOCTYPE html>
        <html><head><title>Dummed Down GeoGuessr</title><link rel='stylesheet' href='/static/style.css'></head><body>
        <div class='container'><h1>Dummed Down GeoGuessr</h1>
        <div id='game-area'>
        <img src='{spot['img']}' alt='Place Image' width='400'>
        <div id='hint'>Hint: {spot['hint']}</div>
        <form action='' method='post'>
            <input type='hidden' name='place_idx' value='{places.index(spot)}'>
            <input type='text' name='guess' placeholder='Guess the location'>
            <input type='submit' value='Guess'>
        </form></div></div></body></html>
        """
        return HTMLResponse(html)
