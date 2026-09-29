-- SQLite --

SELECT  
    sum(Price) AS Gesamtpreis
FROM
    entry AS e, 
    drinks AS d
WHERE 
    e.DrinkID = d.DrinkID
;