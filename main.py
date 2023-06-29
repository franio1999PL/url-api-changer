from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb
import requests

API_URL_SHORTENER = os.getenv("API_URL")
API_KEY_SHORTENER = os.getenv("API_KEY")

# Funkcja do skracania URL
def shorten_url(long_url):
    api_url = API_URL_SHORTENER
    headers = {
        'api-key': API_KEY_SHORTENER,
        'Content-Type': 'application/json'
    }
    data = {
        'link': long_url
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 201:
        json_data = response.json()
        return json_data["data"]["shortUrl"]
        
    else:
        return None

# Połączenie z bazą danych
connection = MySQLdb.Connect(
    host=os.getenv("HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("PASSWORD"),
    db=os.getenv("DATABASE"),
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY"
)

# Tworzenie kursora do interakcji z bazą danych
cursor = connection.cursor()

# Wykonanie zapytania SELECT, aby pobrać wszystkie wiersze z tabeli "Item"
cursor.execute("SELECT * FROM Item")

# Pobranie wszystkich wierszy z wyniku zapytania
rows = cursor.fetchall()

# Iteracja po wierszach
for row in rows:
    item_id = row[0]
    long_url = row[1]

    # Skracanie URL
    short_url = shorten_url(long_url)
    print(f'short_url === {short_url}')

    if short_url:
        # Aktualizacja w bazie danych
        update_query = "UPDATE Item SET url = %s WHERE id = %s"
        cursor.execute(update_query, (short_url, item_id))
        print(f"Item ID: {item_id} - Updated URL: {short_url}")
    else:
        print(f"Item ID: {item_id} - Failed to shorten URL")

# Zamknięcie kursora i połączenia z bazą danych
cursor.close()
connection.close()