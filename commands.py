import sys
from datetime import datetime
from abc import ABC, abstractmethod
import requests
from persistence import BookmarkDatabase


persistence = BookmarkDatabase()


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        pass


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        persistence.create(data)
        return True, None


class ImportGithubStarsCommand(Command):
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
                try:
                    repo = repo_info['repo']
                except:
                    return False, None

                if data['preserve_timestamps']:
                    timestamp = datetime.strptime(
                        repo_info['starred_at'], '%Y-%m-%dT%H:%M:%SZ'
                      )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(self._extract_bookmark_info(repo), timestamp=timestamp)
        return True, bookmarks_imported


class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self, data):
        return True, persistence.list(order_by=self.order_by)


class EditBookmarkCommand(Command):
    def execute(self, data):
        try:
            persistence.update(data['id'], data['update'])
        except:
            return False, None
        return True, None

class DeleteBookmarkCommand(Command):
    def execute(self, data):
        persistence.delete(data)
        return True, None


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()
        return True, None
