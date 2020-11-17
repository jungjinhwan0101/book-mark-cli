import sys
from datetime import datetime
from database import DatabaseManager


db = DatabaseManager('bookmarks.db')


class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table(
            'bookmarks', {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'title': 'TEXT NOT NULL',
                'url': 'TEXT NOT NULL',
                'notes': 'TEXT',
                'date_added': 'TEXT NOT NULL'
            }
        )


class AddBookmarkCommand:
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!'


class ListBookmarksCommand:
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!'


class QuitCommand:
    def execute(self):
        sys.exit()
