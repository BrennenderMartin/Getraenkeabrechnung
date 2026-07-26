import sqlite3
import json

path = "./src/getraenkeabrechnung/backend/"

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
    families = _get_sql("SELECT UserName FROM user ")
    return _get_list_from_sql(families)

def get_image_for_user(user):
    result = _get_sql("SELECT Image FROM user WHERE UserName = ?", (user,))
    path = f"http://localhost:8000/static/images/{result[0][0] if result else ""}" 
    return path

def get_drinks():
    drinks = _get_sql("SELECT DrinkName from drinks")
    return _get_list_from_sql(drinks)

def get_image_for_drink(drink):
    result = _get_sql("SELECT Image FROM drinks WHERE DrinkName = ?", (drink,))
    path = f"http://localhost:8000/static/images/{result[0][0] if result else ""}" 
    return path

if __name__ == "__main__":
    print(get_image_for_drink("Softdrinks"))