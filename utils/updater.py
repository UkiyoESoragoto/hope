from time import sleep

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from config import VERSION


class Updater(QThread):
    check = pyqtSignal(dict)

    def run(self):
        while 1:
            ret = check_on_github(
                VERSION,
                user='ukiyoesoragoto',
                repository='hope'
            )
            if ret:
                self.check.emit(ret)
            sleep(3600 * 12)


def check_on_github(
        now_ver: str,
        url_str: str = '',
        user: str = '',
        repository: str = '',
):
    """Check with api.github.com

    :param now_ver: Now version string, format: '0.0.0'
    :param url_str: Github repository releases url string
    :param user: Github user name
    :param repository: Github repository name
    :return:
    """
    # sleep(10)
    try:
        response = requests.get(
            url=(url_str if url_str
                 else f'https://api.github.com/repos/{user}/{repository}/releases')
        )
        versions = response.json()
    except Exception as e:
        print(e)
        versions = []
    for version in versions:
        if update_available(version.get('tag_name', ''), now_ver):
            return version_info(version)
    return {}


def update_available(ver_str: str, now_ver: str):
    """Check update is available

    :param ver_str: Version string to compare, format: '0.0.0'
    :param now_ver: Now version string, format: '0.0.0'
    :return:
        bool:True for Update is available / False for No update is available
    """
    if not ver_str or not now_ver:
        return False
    try:
        version = [int(ver) for ver in ver_str.split('.')[:3]]
    except ValueError as e:
        print(e)
        return False

    now_version = [int(ver) for ver in now_ver.split('.')[:3]]

    try:
        for x in range(3):
            if version[x] > now_version[x]:
                return True
            if version[x] < now_version[x]:
                return False
            if version[x] == now_version[x]:
                continue
    except IndexError as e:
        print(e)
        return False
    return False


def version_info(ver: dict):
    return {
        'name': ver.get('name', ''),
        'desc': ver.get('body', ''),
        'version': ver.get('tag_name', ''),
        'published_at': ver.get('published_at', ''),
        'html_url': ver.get('html_url', ''),
        'assets': [
            {
                'url': asset.get('browser_download_url', ''),
                'name': asset.get('name')
            } for asset in ver.get('assets', [])
        ]
    }
