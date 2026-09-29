import matplotlib.pyplot as plt
from src.getraenkeabrechnung.backend.main import (
    _get_sql,
    _get_list_from_sql,
    get_gesamtbetrag
)

plt.figure(num="Ausgaben nach verschiedenen Filtern")

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

def command(filters):
    return f"""
SELECT  
    {filters}Name,
    sum(Price) AS Gesamtpreis
FROM
    entry AS e, 
    user AS u, 
    drinks AS d
WHERE 
    e.UserID = u.UserID AND
    e.DrinkID = d.DrinkID
GROUP BY {filters}Name
ORDER BY Gesamtpreis DESC
;
"""


users = _get_list_from_sql(_get_sql("SELECT UserName FROM user"))
drinks = _get_list_from_sql(_get_sql("SELECT DrinkName FROM drinks"))
ges = round(_get_sql(
    "SELECT sum(Price) FROM entry AS e, drinks AS d WHERE e.DrinkID = d.DrinkID;"
)[0][0], 2)

filters = ["Drink", "User"]

print(f"{users = }, \n{drinks = }, \n{ges = }, \n{filters = }\n")

for i, user in enumerate(users):
    df = _get_sql(command_for_user(user))
    items = _get_list_from_sql(df)
    prices = _get_list_from_sql(df, 1)
    user_ges = get_gesamtbetrag(user)

    labels = [f"{items[i]} ({round(prices[i], 2)} €)" for i in range(len(prices))]
    print(f"{user}: {labels}")

    a_users = _get_sql("SELECT COUNT(*) FROM user")[0][0]
    rows = 2
    if a_users % rows == 0:
        columns = int(a_users / rows)
    else:
        columns = a_users
    
    plt.subplot(rows + 1, columns, len(filters) + i + 1)
    plt.pie(x=prices, labels=labels)
    plt.title(f"{user} ({user_ges} €)")

print()

for i, filteri in enumerate(filters):
    df = _get_sql(command(filteri))
    items = _get_list_from_sql(df)
    prices = _get_list_from_sql(df, 1)

    labels = [f"{items[i]} ({round(prices[i], 2)} €)" for i in range(len(prices))]
    print(f"{filteri}: {labels}")

    plt.subplot(rows + 1, columns, i + 1)
    plt.pie(x=prices, labels=labels)
    plt.title(f"{filteri}s ({ges} €)")

print()

plt.show()
