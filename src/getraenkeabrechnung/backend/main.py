import sqlite3
import json

path = "./src/getraenkeabrechnung/backend/"

def get_sql(command: str) -> list:
    database_file = f"{path}db.sqlite"

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute(command)
    output = cursor.fetchall()

    cursor.close()
    conn.close()

    return output

def save_sql(filename, sqldata):
    output_file = f"{path}{filename}"
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(sqldata, json_file, indent=4, ensure_ascii=False)
    
    print("File saved!")


if __name__ == "__main__":
    print(get_sql(
        "SELECT UserName, Image FROM user"
    ))