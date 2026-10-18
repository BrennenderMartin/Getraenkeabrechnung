import matplotlib.pyplot as plt
from src.getraenkeabrechnung.backend.main import (
    _get_sql,
    _get_list_from_sql
)

times = [ordertime[11:16] for ordertime in _get_list_from_sql(_get_sql("""
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
        d.AdultTag = True
    """
))]
times.sort()

df = {}

for i, item in enumerate(times):
    if not item == times[i -1]:
        df[item] = 1
    else:
        df[item] += 1

plt.bar(
    df.keys(), 
    df.values(), 
    width = 0.8
)
plt.show()

print(df)
