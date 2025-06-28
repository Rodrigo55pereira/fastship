import sqlite3
from typing import Any

from app.schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def __init__(self):
        # Make the connection
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    # Create table if not exists
    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """,
        )

    def create(self, shipment: ShipmentCreate) -> int:
        # Find a new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        # 2. Add shipment data
        self.cur.execute(
            """
               INSERT INTO shipment
               VALUES(:id, :content, :weight, :status)
            """,
            {"id": new_id, **shipment.model_dump(), "status": "placed"},
        )
        self.conn.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        # 3. Read a shipment by id
        self.cur.execute(
            """
                SELECT * FROM shipment
                WHERE id = ?
            """,
            (id,),
        )
        row = self.cur.fetchone()

        return (
            {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3],
            }
            if row
            else None
        )

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any] | None:
        # 4. Update a shipment
        self.cur.execute(
            """
            UPDATE shipment SET status = :status
            WHERE id = :id
            """,
            {"id": id, **shipment.model_dump()},
        )
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute(
            """
                DELETE FROM shipment
                WHERE id = ?
            """,
            (id,),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
