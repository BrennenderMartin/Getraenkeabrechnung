import sqlite3
import json
import pandas as pd
import matplotlib.pyplot as plt
from src.getraenkeabrechnung.backend.main import (
    _exec_sql,
    _get_sql
)

df = pd.DataFrame(
    _get_sql(
        """
        SELECT 
            DrinkName, 
            count(DrinkName)
        FROM
            entry AS e, 
            user AS u, 
            drinks AS d
        WHERE 
            e.UserID = u.UserID AND
            e.DrinkID = d.DrinkID 
        GROUP BY DrinkName
        ;
        """
    ),
    columns=["Drink", "Count"]
)

print(df)

df.plot(kind="bar", x="Drink", y="Count")

plt.show()