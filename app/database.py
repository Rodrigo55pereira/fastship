import json
import sqlite3

# Make the connection
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# 1. Create Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipment (
        id INTEGER,
        content TEXT,
        weight REAL,
        status TEXT
    )
"""
)

# Close the connection when done
connection.close()


shipments = {}  # type:ignore

with open("shipments.json") as json_file:
    data = json.load(json_file)
    for value in data:
        shipments[value["id"]] = value


def save():
    with open("shipments.json", "w") as json_file:
        json.dump(list(shipments.values()), json_file)
