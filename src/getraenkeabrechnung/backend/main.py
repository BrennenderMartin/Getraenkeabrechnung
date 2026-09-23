import sqlite3
import json
from uuid import uuid4

path = "./src/getraenkeabrechnung/backend/"

def _exec_sql(command: str, table = None, params: tuple = ()):
    database_file = f"{path}db.sqlite"

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute(command, params)
    conn.commit()

    if table is not None:
        cursor.execute(f"SELECT * FROM {table}")
        output = cursor.fetchall()
    else:
        output = f"No output for command '{command}' wanted"

    cursor.close()
    conn.close()

    return output

def _get_sql(command: str, params: tuple = ()) -> list:
    database_file = f"{path}db.sqlite"

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute(command, params)
    output = cursor.fetchall()

    cursor.close()
    conn.close()

    return output

def _get_list_from_sql(output):
    retList = []
    for item in output:
        retList.append(item[0])
    return retList

def _save_sql(filename, sqldata):
    output_file = f"{path}{filename}"
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(sqldata, json_file, indent=4, ensure_ascii=False)
    
    print("File saved!")



def get_families():
    return _get_list_from_sql(_get_sql("SELECT UserName FROM user "))

def get_image_for_user(user):
    result = _get_sql("SELECT Image FROM user WHERE UserName = ?", (user,))
    path = f"/static/images/{result[0][0] if result else ""}" 
    return path



def get_drinks(restriction: bool = False):
    """Restriction, meaning if children have access to said Product, defaults to False so all drinks will be shown, if given as True, the drinks will be restricted and only non alcoholical drinks will be shown"""
    if restriction is False:
        drinks = _get_sql("SELECT DrinkName from drinks ORDER BY AdultTag")
    else:
        drinks = _get_sql("SELECT DrinkName from drinks WHERE AdultTag = 0")
    return _get_list_from_sql(drinks)

def get_image_for_drink(drink):
    result = _get_sql("SELECT Image FROM drinks WHERE DrinkName = ?", (drink,))
    path = f"/static/images/{result[0][0] if result else ""}" 
    return path

def get_price_for_drink(drink):
    return _get_sql("SELECT Price FROM drinks WHERE DrinkName = ?", (drink,))[0][0]

def get_drink_id(drink):
    return _get_sql("SELECT DrinkID FROM drinks WHERE DrinkName = ?", (drink,))[0][0]

def return_drink(name, drink):
    Id = hex(_get_sql("SELECT count(*) FROM entry")[0][0])[2:]
    UserID = _get_sql("SELECT UserID FROM user WHERE UserName = ?", (name,))[0][0]
    DrinkID = _get_sql("SELECT DrinkID FROM drinks WHERE DrinkName = ?", (drink,))[0][0]
    
    _exec_sql(f"INSERT into entry values('{uuid4()}-{Id}', '{UserID}', '{DrinkID}', CURRENT_TIMESTAMP)", "entry")
    #print(f"{name = }, {drink = }, {Id = }, {UserID = }, {DrinkID = }") # Output = "Jung Softdrinks"



def get_AdultTag(user):
    return _get_sql("SELECT AdultTag FROM user WHERE UserName = ?", (user,))[0][0]

def set_AdultTag(user):
    return _exec_sql(f"UPDATE user SET AdultTag = {not get_AdultTag(user)} WHERE UserName = '{user}'", "user")

def get_gesamtbetrag(user):
    ges = _get_sql(f"SELECT sum(d.Price) AS Gesamtbetrag FROM entry AS e, user AS u, drinks AS d WHERE e.UserID = u.UserID AND e.DrinkID = d.DrinkID AND u.UserName = '{user}';")[0][0]
    if ges is not None:
        return round(ges, 2)
    else:
        return 0

def add_drink(name: str, price: int, image: str, adulttag: bool):
    Id = f"{uuid4()}-{_get_sql("SELECT count(*) FROM drinks")[0][0] + 1}"
    return _exec_sql(f"INSERT INTO drinks VALUES ('{Id}', '{name}', '{price}', '{image}', {adulttag})", "drinks")

def add_user(name: str, adults: int, children: int, adulttag: bool, image: str = None):
    Id = f"{uuid4()}-{100 - _get_sql("SELECT count(*) FROM user")[0][0]}"
    return _exec_sql(f"INSERT INTO user VALUES ('{Id}', '{name}', '{adults}', '{children}', '{image}', {adulttag})", "user")

if __name__ == "__main__":
    print()
