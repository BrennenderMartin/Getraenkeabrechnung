-- SQLite --

SELECT 
    UserName,
    DrinkName, 
    count(DrinkName) AS Anzahl,
    Price,
    sum(Price) AS Gesamtpreis
FROM
    entry AS e, 
    user AS u, 
    drinks AS d
WHERE 
    e.UserID = u.UserID AND
    e.DrinkID = d.DrinkID AND
    UserName = "Jung"
GROUP BY DrinkName
ORDER BY Gesamtpreis DESC
;