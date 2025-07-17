from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load data from the JSON file
with open('restaurants.json', 'r') as f:
    restaurants = json.load(f)["elements"]  # Data is inside the "elements" key

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    cuisine = request.args.get('cuisine')
    open_now = request.args.get('open_now')

    filtered = restaurants

    # Filter by cuisine if specified
    if cuisine:
        filtered = [
            r for r in filtered
            if 'cuisine' in r['tags'] and cuisine.lower() in r['tags']['cuisine'].lower()
        ]

    # Filter by open_now if requested (naively checks if "Su" is present in opening_hours)
    if open_now is not None:
        is_open = open_now.lower() == "true"
        filtered = [
            r for r in filtered
            if 'opening_hours' in r['tags'] and check_open_hours(r['tags']['opening_hours'], is_open)
        ]

    return jsonify(filtered)


@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    for r in restaurants:
        if r["id"] == restaurant_id:
            return jsonify(r)
    return jsonify({"error": "Restaurant not found"}), 404


def check_open_hours(opening_hours, is_open):
    # Very basic placeholder logic: returns True if 'Su' in hours and open_now is True
    if is_open:
        return "Su" in opening_hours
    else:
        return True  # If not filtering for "open now", return all

if __name__ == '__main__':
    app.run(debug=True)
