import sqlite3
import json
import pandas as pd
import matplotlib.pyplot as plt
from src.getraenkeabrechnung.backend.main import (
    _get_sql,
    _get_list_from_sql,
    get_gesamtbetrag
)

command = """
SELECT  
    DrinkName,
    sum(Price) AS Gesamtpreis
FROM
    entry AS e, 
    user AS u, 
    drinks AS d
WHERE 
    e.UserID = u.UserID AND
    e.DrinkID = d.DrinkID
GROUP BY DrinkName
ORDER BY Gesamtpreis DESC
;
"""


drinks = _get_list_from_sql(_get_sql("SELECT DrinkName FROM drinks"))
print(f"{drinks = }")

ges = round(_get_sql(
    "SELECT sum(Price) AS Gesamtpreis FROM entry AS e, drinks AS d WHERE e.DrinkID = d.DrinkID;"
)[0][0], 2)
dfl = _get_sql(command)
items = _get_list_from_sql(dfl)
prices = _get_list_from_sql(dfl, 1)

labels = [f"{items[i]} ({round(prices[i], 2)} €)" for i in range(len(prices))]
print(labels)

plt.pie(x=prices, labels=labels)
plt.title(f"Gesamtausgaben ({ges} €)")

print()

plt.show()
