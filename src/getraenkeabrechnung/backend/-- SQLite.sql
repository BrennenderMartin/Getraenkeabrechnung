-- SQLite --

SELECT 
    u.UserName AS Name, 
    sum(d.Price) AS Gesamtbetrag
FROM 
    entry AS e, 
    user AS u, 
    drinks AS d
WHERE 
    e.UserID = u.UserID AND
    e.DrinkID = d.DrinkID
GROUP BY u.UserID
--HAVING u.UserName = "Jung"
ORDER BY 2 DESC;
