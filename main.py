from database import DatabaseManager


db = DatabaseManager('test.db')
columns = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'title': 'TEXT NOT NULL',
    'url': 'TEXT NOT NULL',
    'notes': 'TEXT',
    'date_added': 'TEXT NOT NULL'
}
db.create_table('test', columns)
db.add('test', {'title': 'test_title', 'url': 'www.test.com'})
cursor = db.select('test', {'title': 'test_title'})
print(cursor.fetchall())
db.delete('test', {'title': 'test_title'})