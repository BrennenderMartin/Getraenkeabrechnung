import sqlite3
import json
import pandas as pd
import matplotlib.pyplot as plt
from src.getraenkeabrechnung.backend.main import (
    _get_sql,
    _get_list_from_sql,
    get_gesamtbetrag
)

def command_for_user(user):
    return f"""
SELECT  
    DrinkName,
    sum(Price) AS Gesamtpreis
FROM
    entry AS e, 
    user AS u, 
    drinks AS d
WHERE 
    e.UserID = u.UserID AND
    e.DrinkID = d.DrinkID AND
    UserName = '{user}'
GROUP BY DrinkName
ORDER BY Gesamtpreis DESC
;
"""

users = _get_list_from_sql(_get_sql("SELECT UserName FROM user"))
drinks = _get_list_from_sql(_get_sql("SELECT DrinkName FROM drinks"))
print(f"{users = }, {drinks = }")

for i, user in enumerate(users):
    dfl = _get_sql(command_for_user(user))
    items = _get_list_from_sql(dfl)
    prices = _get_list_from_sql(dfl, 1)
    ges = get_gesamtbetrag(user)
    labels = [f"{items[i]} ({round(prices[i], 2)} €)" for i in range(len(prices))]
    print(labels)
    a_users = _get_sql("SELECT COUNT(*) FROM user")[0][0]
    rows = 2
    if a_users % rows == 0:
        columns = int(a_users / rows)
    else:
        columns = a_users
    plt.subplot(rows, columns, i + 1)
    plt.pie(x=prices, labels=labels)
    plt.title(f"{user} ({ges} €)")

print()

plt.show()
