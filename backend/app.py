from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )

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
        restaurant['avg_saltiness'] or 5,  # Default to neutral if None
        restaurant['avg_sweetness'] or 5,
        restaurant['avg_spiciness'] or 5,
        restaurant['avg_sourness'] or 5,
        restaurant['avg_umaminess'] or 5
    ])
    
    return np.linalg.norm(user_tastes - restaurant_tastes)

# Route to accept user preferences and return top 5 restaurant matches
@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_location = data.get("location")
    
    if not user_location:
        return jsonify({"error": "Location is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to find the top 5 matching restaurants
    query = """
        SELECT r.*
        FROM restaurants r
        WHERE r.location = %s
        ORDER BY 
            ABS(%s - COALESCE(r.avg_saltiness, 5)) +
            ABS(%s - COALESCE(r.avg_sweetness, 5)) +
            ABS(%s - COALESCE(r.avg_spiciness, 5)) +
            ABS(%s - COALESCE(r.avg_sourness, 5)) +
            ABS(%s - COALESCE(r.avg_umaminess, 5)) 
        LIMIT 5;
    """

    cursor.execute(query, (
        user_location,
        data["saltiness"],
        data["sweetness"],
        data["spiciness"],
        data["sourness"],
        data["umaminess"]
    ))
    
    restaurants = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert result to JSON
    restaurant_list = [
        {
            "restaurant_id": r[0],
            "name": r[1],
            "location": r[2],
            "cuisine": r[3],
            "avg_saltiness": r[4],
            "avg_sweetness": r[5],
            "avg_spiciness": r[6],
            "avg_sourness": r[7],
            "avg_umaminess": r[8],
            "google_maps_id": r[9]
        }
        for r in restaurants
    ]

    return jsonify(restaurant_list)


if __name__ == '__main__':
    app.run(debug=True)
