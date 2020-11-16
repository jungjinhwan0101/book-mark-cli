from database import DatabaseManager


db = DatabaseManager('test.db')
columns = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'title': 'TEXT NOT NULL',
    'url': 'TEXT NOT NULL',
    'notes': 'TEXT'
}
db.create_table('test', columns)
