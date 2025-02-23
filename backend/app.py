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

# Similarity calculation using Euclidean distance
def calculate_similarity(user_prefs, restaurant):
    user_tastes = np.array([
        user_prefs['saltiness'],
        user_prefs['sweetness'],
        user_prefs['spiciness'],
        user_prefs['sourness'],
        user_prefs['umaminess']
    ])
    
    restaurant_tastes = np.array([
        restaurant.get('avg_saltiness', 5),
        restaurant.get('avg_sweetness', 5),
        restaurant.get('avg_spiciness', 5),
        restaurant.get('avg_sourness', 5),
        restaurant.get('avg_umaminess', 5)
    ])
    
    return np.linalg.norm(user_tastes - restaurant_tastes)

# Route to accept user preferences and return top 5 restaurant matches
@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_location = data.get("location")
    print(data)
    if not user_location:
        return jsonify({"error": "Location is required"}), 400
    # Fetch restaurants from Supabase
    response = supabase.table("restaurants").select("*").eq("location", user_location).execute()
    print(response)
    if not response.data:
        return jsonify({"error": "No restaurants found in this location"}), 404

    restaurants = response.data

    # Calculate similarity for each restaurant
    for restaurant in restaurants:
        restaurant['similarity'] = calculate_similarity(data, restaurant)

    # Sort by similarity and return top 5
    top_matches = sorted(restaurants, key=lambda x: x['similarity'])[:5]

    return jsonify(top_matches)

if __name__ == '__main__':
    app.run(debug=True)
