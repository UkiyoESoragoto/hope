from unittest import TestCase, mock

from utils import updater

REPOSITORY_URL = 'https://api.github.com/repos/ukiyoesoragoto/hope/releases'
NOW_VER_L = '0.0.0'  # less than
NOW_VER_G = '1.0.0'  # greater than
NOW_VER_E = '0.3.0'  # equal
USER = 'ukiyoesoragoto'
REPOSITORY = 'hope'


class MockResponse(object):
    def __init__(self, content):
        self.content = content

    def json(self):
        return self.content


def mock_request_get(url):
    if url == REPOSITORY_URL:
        return MockResponse([
            {
                'html_url': 'url',
                'tag_name': '0.3.0',
                'name': 'name',
                'published_at': 'published_at',
                'assets': [
                    {
                        'name': 'name',
                        'browser_download_url': 'url'
                    },
                    {
                        'name': 'name',
                        'browser_download_url': 'url'
                    }
                ],
                'body': 'body'
            }
        ])

    if url == 'error_tag_name':
        return MockResponse([{'tag_name': 'v0.3.0'}])

    return 'unhandled request %s' % url


class TestUtils(TestCase):
    @mock.patch(
        'requests.get',
        mock.Mock(
            side_effect=mock_request_get
        )
    )
    def test_check_on_github_same_return_with_diff_args(self):
        self.assertEqual(
            updater.check_on_github(
                now_ver=NOW_VER_L,
                user=USER,
                repository=REPOSITORY
            ),
            updater.check_on_github(now_ver=NOW_VER_L, url_str=REPOSITORY_URL)
        )

    @mock.patch(
        'requests.get',
        mock.Mock(
            side_effect=mock_request_get
        )
    )
    def test_check_on_github_now_version_less_than(self):
        except_ret = {
            'name': 'name',
            'desc': 'body',
            'version': '0.3.0',
            'published_at': 'published_at',
            'html_url': 'url',
            'assets': [
                {
                    'url': 'url',
                    'name': 'name'
                },
                {
                    'url': 'url',
                    'name': 'name'
                }
            ]}

        self.assertEqual(
            except_ret,
            updater.check_on_github(now_ver=NOW_VER_L, url_str=REPOSITORY_URL)
        )

    @mock.patch(
        'requests.get',
        mock.Mock(
            side_effect=mock_request_get
        )
    )
    def test_check_on_github_now_version_greater_than(self):
        except_ret = {}
        self.assertEqual(
            except_ret,
            updater.check_on_github(now_ver=NOW_VER_G, url_str=REPOSITORY_URL)
        )

    @mock.patch(
        'requests.get',
        mock.Mock(
            side_effect=mock_request_get
        )
    )
    def test_check_on_github_now_version_equal(self):
        except_ret = {}
        self.assertEqual(
            except_ret,
            updater.check_on_github(now_ver=NOW_VER_G, url_str=REPOSITORY_URL)
        )

    @mock.patch(
        'requests.get',
        mock.Mock(
            side_effect=mock_request_get
        )
    )
    def test_check_on_github_with_error_now_ver(self):
        self.assertRaises(
            ValueError,
            updater.check_on_github,
            now_ver='v1.0.0',
            url_str=REPOSITORY_URL
        )

    @mock.patch(
        'requests.get',
        mock.Mock(
            side_effect=mock_request_get
        )
    )
    def test_check_on_github_with_error_tag_name(self):
        except_ret = {}
        self.assertEqual(
            except_ret,
            updater.check_on_github(now_ver=NOW_VER_G, url_str='error_tag_name')
        )
