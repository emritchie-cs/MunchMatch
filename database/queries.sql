-- queries for later
-- finds restaurants in same location as user
-- sorts them by how close the taste profile is to user user preferences
-- returns top 5 matches

/*
SELECT r.*
FROM restaurants r
JOIN user_preferences u ON u.location = r.location
ORDER BY 
    ABS(u.saltiness - r.avg_saltiness) +
    ABS(u.sweetness - r.avg_sweetness) +
    ABS(u.spiciness - r.avg_spiciness) +
    ABS(u.sourness - r.avg_sourness) +
    ABS(u.umaminess - r.avg_umaminess) 
LIMIT 5;*/