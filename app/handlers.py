import logging
import os
import shutil
import sqlite3
import subprocess
from typing import Optional, Awaitable

from tornado.web import RequestHandler

from app.constants import CHROME, GOOGLE_CHROME, OPEN_FIREFOX, KILL_CHROME, KILL_FIREFOX, CHROME_STORAGE_PATH, \
    FIREFOX_STORAGE_PATH

logger = logging.getLogger("app")


def start_browser(url, browser):
    subprocess.Popen(f'open -a "{browser}" {url}', shell=True)


def kill_browser(browser):
    subprocess.Popen(f'killall {browser}', shell=True)


def run_query(path, query):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def clean_history(history_db, query):
    run_query(history_db, query)


def clean_cookies(cookies_db, query):
    run_query(cookies_db, query)


def delete_folder_contents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def cleanup_browser(browser):
    if browser == CHROME:
        data_path = os.path.expanduser('~') + CHROME_STORAGE_PATH
        delete_folder_contents(data_path)

    else:
        data_path = os.path.expanduser('~') + FIREFOX_STORAGE_PATH
        delete_folder_contents(data_path)


class StartHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        # logger.info()
        browser = self.get_argument('browser', None)
        url = self.get_argument('url', None)
        if browser is not None and url is not None:
            if browser == CHROME:
                start_browser(url, GOOGLE_CHROME)
            else:
                start_browser(url, OPEN_FIREFOX)


class StopHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        browser = self.get_argument('browser', None)
        if browser is not None:
            if browser == CHROME:
                kill_browser(KILL_CHROME)
            else:
                kill_browser(KILL_FIREFOX)


class CleanupHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        browser = self.get_argument('browser', None)
        if browser is not None:
            cleanup_browser(browser)


class GetUrlHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        browser = self.get_argument('browser', None)
        if browser is not None:
            if browser == CHROME:
                pass
            else:
                pass
