from sqlite3 import Error
import sqlite3

class Database:
    def __init__(self, database_name='image_database.db'):
        self.database_name = database_name
        self.conn = None
    
    def create_database(self):
        self.conn = None 
        try:
            self.conn = sqlite3.connect(self.database_name)
            return self.conn 
        except Error as e:
            print(e) 
        
        return self.conn 

    def create_table(self):
        sql_create_table_script = "CREATE TABLE IF NOT EXISTS image (uuid string PRIMARY KEY, path text, image_name text)"

        try:
            c =  self.conn.cursor()
            c.execute(sql_create_table_script)
        except Error as e:
            print(e)

if __name__ == '__main__':
    db = Database()
    db.create_database()
    db.create_table()