import sqlite3
import json
import pandas as pd
import matplotlib.pyplot as plt
from src.getraenkeabrechnung.backend.main import (
    _exec_sql,
    _get_sql,
    _get_list_from_sql
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

def df_for_user(user):
    command = command_for_user(user)
    return pd.DataFrame(
        _get_sql(command),
        columns=["Drink", "Count"],
        index=_get_list_from_sql(_get_sql(command))
    )

users = _get_list_from_sql(_get_sql("SELECT UserName FROM user"))

for i, user in enumerate(users):
    df = df_for_user(user)
    print(df.loc[:, "Count"])
    plt.subplot(1, 2, i + 1)
    plt.pie(x=df.loc[:, "Count"], labels=df.loc[:, "Drink"])
    plt.title(f"Ausgaben für Nutzer {user}")


plt.show()
