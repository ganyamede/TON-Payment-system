from typing import Union
import sqlite3

class Database:
    """
    Initialize the database connection and set up query parameters.

    :param table_name: The name of the table for operations.
    :param columns: The names of columns for selection, update, or insertion.
    :param values: The values for insertion or updating.
    :param where_clause: The condition for filtering records.
    """
    
    def __init__(self, table_name: str=None, columns: Union[list, str]=None, values: Union[list, str]=None, where_clause: str=None) -> None:
        with sqlite3.connect('core/storage/path/ton.db', check_same_thread=False) as self.connection:
            self.db = self.connection.cursor()
            self.table_name = table_name
            self.where_clause = where_clause
            self.columns = columns
            self.values = values
        
    def commit(self):
        """Commit changes to the database."""
        if self.connection:
            self.connection.commit()

class Select(Database):
    def execute(self) -> None:
        columns_str = ', '.join(self.columns) if isinstance(self.columns, list) else self.columns
        query = f"SELECT {columns_str} FROM {self.table_name}"
        if self.where_clause:
            query += f" WHERE {self.where_clause}"
        result = self.db.execute(query).fetchall() 
        return result

class Update(Database):
    def execute(self) -> None:
        set_clause = ', '.join([f"{col} = ?" for col in self.columns])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.where_clause}"
        self.db.execute(query, self.values)
        self.commit()

class Insert(Database):
    def execute(self) -> None:
        """Insert data into a table."""
        columns_str = ', '.join(self.columns)
        placeholders = ', '.join(['?' for _ in self.values])
        query = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"
        self.db.execute(query, self.values)
        self.commit()