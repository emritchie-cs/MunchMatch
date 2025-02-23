from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
from supabase import create_client, Client

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:8000"]}})

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://hnphrbhajwsclrmexqbi.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhucGhyYmhhandzY2xybWV4cWJpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyNjU3MzksImV4cCI6MjA1NTg0MTczOX0.KGDIw3QKWC9s5s8ak0H4Tm8vAYKyYTSwZ3i_JO9pw_Q")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Global variable to store user intake data
user_preferences_data = {}

# Similarity calculation using Euclidean distance (assumes all required fields exist)
def calculate_similarity(restaurant):
    global user_preferences_data  # use the global variable
    user_tastes = np.array([
        float(user_preferences_data['sweetness']),
        float(user_preferences_data['saltiness']),
        float(user_preferences_data['spiciness']),
        float(user_preferences_data['sourness']),
        float(user_preferences_data['umaminess'])
    ])
    
    restaurant_tastes = np.array([
        float(restaurant['avg_saltiness']),
        float(restaurant['avg_sweetness']),
        float(restaurant['avg_spiciness']),
        float(restaurant['avg_sourness']),
        float(restaurant['avg_umaminess'])
    ])
    
    # Debug prints to confirm values
    #print(f"User Preferences: {user_tastes}")
    #print(f"Restaurant {restaurant.get('name', 'Unknown')} Tastes: {restaurant_tastes}")
    
    distance = np.linalg.norm(user_tastes - restaurant_tastes)
    #print(distance)
    return distance


# Endpoint to accept user preferences (intake)
@app.route('/api/intake', methods=['POST'])
def intake():
    global user_preferences_data
    data = request.get_json()
    print("Received intake data:", data)
    # Store the full payload (including location and taste values)
    user_preferences_data = data
    return jsonify({'status': 'preferences stored'})

# Endpoint to return top 5 recommended restaurants
@app.route('/api/recommend', methods=['POST'])
def recommend():
    global user_preferences_data
    # Use stored preferences if available; otherwise, fall back to request payload.
    data = request.get_json()
    user_location = data.get("location")
    if not user_location:
        return jsonify({"error": "Location is required"}), 400

    # Fetch restaurants from Supabase based on location
    response = supabase.table("restaurants").select("*").eq("location", user_location).execute()
    if not response.data:
        return jsonify({"error": "No restaurants found in this location"}), 404

    restaurants = response.data
    #(restaurants)
    #print(f"Retrieved {len(restaurants)} restaurants from database.")

    # (Optional) Ensure required restaurant taste attributes exist;
    # here we assume they do exist in your database.

    # Calculate similarity for each restaurant
    valid_restaurants = []
    for restaurant in restaurants:
        try:
            restaurant['similarity'] = calculate_similarity(restaurant)
            valid_restaurants.append(restaurant)
        except Exception as e:
            print(f"Skipping {restaurant.get('name', 'Unknown')}: {e}")
            continue

    # Sort by similarity (lower distance means more similar) and return top 5
    top_matches = sorted(valid_restaurants, key=lambda x: x['similarity'])[:5]
    #print("Top 5 Matches:", [(r['name'], r['similarity']) for r in top_matches])
    return jsonify(top_matches)

if __name__ == '__main__':
    app.run(debug=True)
