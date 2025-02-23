CREATE TABLE user_preferences (
    user_id SERIAL PRIMARY KEY,
    location VARCHAR(255),
    saltiness INT CHECK (saltiness BETWEEN 0 AND 10),
    sweetness INT CHECK (sweetness BETWEEN 0 AND 10),
    spiciness INT CHECK (spiciness BETWEEN 0 AND 10),
    sourness INT CHECK (sourness BETWEEN 0 AND 10),
    umaminess INT CHECK (sourness BETWEEN 0 AND 10)
);

CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    cuisine VARCHAR(100),
    avg_saltiness FLOAT DEFAULT NULL,
    avg_sweetness FLOAT DEFAULT NULL,
    avg_spiciness FLOAT DEFAULT NULL,
    avg_sourness FLOAT DEFAULT NULL,
    avg_umaminess FLOAT DEFAULT NULL,
    google_maps_id VARCHAR(100) UNIQUE NOT NULL
);

SELECT * FROM restaurants;

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    saltiness_score INT CHECK (saltiness_score BETWEEN 0 AND 10),
    sweetness_score INT CHECK (sweetness_score BETWEEN 0 AND 10),
    spiciness_score INT CHECK (spiciness_score BETWEEN 0 AND 10),
    sourness_score INT CHECK (spiciness_score BETWEEN 0 AND 10),
    umaminess_score INT CHECK (spiciness_score BETWEEN 0 AND 10)
);

ALTER TABLE reviews 
ADD CONSTRAINT fk_reviews_restaurants 
FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE;