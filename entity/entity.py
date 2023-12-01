# entity defn

from repository import db

class Entity:
    table_name: str
    def __init__(self, table_name, **kwargs):
        self.table_name = table_name
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_") and k != "table_name"}
    
    def save(self):
        cursor = db.get_cursor()
        columns = list(self.__dict__.keys())
        columns.remove("id")
        columns.remove("table_name")
        values = [getattr(self, column) for column in columns]
        query = f"INSERT INTO {self.table_name}s ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))}) RETURNING id"
        cursor.execute(query, values)
        self.id = cursor.fetchone()[0]
        db.commit()
    
    def update(self):
        cursor = db.get_cursor()
        columns = list(self.__dict__.keys())
        columns.remove("id")
        values = [getattr(self, column) for column in columns]
        values.append(self.id)
        query = f"UPDATE {self.table_name}s SET {', '.join([f'{column} = %s' for column in columns])} WHERE id = %s"
        cursor.execute(query, values)
        db.commit()

    def get(self, id):
        cursor = db.get_cursor()
        query = f"SELECT * FROM {self.table_name}s WHERE id = %s"
        cursor.execute(query, (id,))
        data = cursor.fetchone()
        if data is None:
            return None
        return self.__class__(**dict(zip([column.name for column in cursor.description], data)))

    def getall(self):
        cursor = db.get_cursor()
        query = f"SELECT * FROM {self.table_name}s"
        cursor.execute(query)
        data = cursor.fetchall()
        # make a list of objects with attributes from the data
        return [self.__class__(**dict(zip([column.name for column in cursor.description], row))) for row in data]
    
    def __str__(self):
        return f"{self.table_name}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
    
    def __repr__(self):
        return str(self)
