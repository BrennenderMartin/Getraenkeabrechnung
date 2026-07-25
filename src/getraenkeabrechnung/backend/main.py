import sqlite3
import json

path = "./src/getraenkeabrechnung/backend/"

def get_sql(command: str, params: tuple = ()) -> list:
    database_file = f"{path}db.sqlite"

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute(command, params)
    output = cursor.fetchall()

    cursor.close()
    conn.close()

    return output

def save_sql(filename, sqldata):
    output_file = f"{path}{filename}"
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(sqldata, json_file, indent=4, ensure_ascii=False)
    
    print("File saved!")

def get_image_for_user(user):
    result = get_sql("SELECT Image FROM user WHERE UserName = ?", (user,))
    path = f"http://localhost:8000/static/images/{result[0][0] if result else ""}" 
    return path

if __name__ == "__main__":
    print(get_image_for_user("Jung"))