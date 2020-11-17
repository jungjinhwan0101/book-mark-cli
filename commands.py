import sys
from datetime import datetime

import requests

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


class ImportGithubStarsCommand:
    def _extract_bookmark_info(self, repo):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description']
        }

    def execute(self, data):
        bookmarks_imported = 0
        github_username = data['github_username']
        next_page_of_results = f'https://api.github.com/users/{github_username}/starred'

        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={'Accept': 'application/vnd.github.v3.star+json'}
            )
            next_page_of_results = stars_response.links.get('next', {}).get('url')

            for repo_info in stars_response.json():
                repo = repo_info['repo']

                if data['preserve_timestamps']:
                    timestamp = datetime.strptime(
                        repo_info['starred_at'], '%Y-%m-%dT%H:%M:%SZ'
                      )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(self._extract_bookmark_info(repo), timestamp=timestamp)
        return f'Imported {bookmarks_imported} bookmarks from starred repos!'


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
