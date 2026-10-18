-- SQLite --

SELECT
    OrderTime
FROM
    drinks AS d,
    entry AS e,
    user AS u 
WHERE 
    e.UserID = u.UserID AND
    e.DrinkID = d.DrinkID AND
    UserName = "Jung" AND
    DrinkName = "Shots"
