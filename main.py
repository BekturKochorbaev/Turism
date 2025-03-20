import sqlite3

# Откройте базу данных
conn = sqlite3.connect('ourcountry/db.sqlite3')
cursor = conn.cursor()

# Показать таблицы в базе данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Таблицы в базе данных:")
for table in tables:
    print(table)

conn.close()
