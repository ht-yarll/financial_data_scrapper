from selenium import webdriver
from selenium import __version__
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote import remote_connection

from time import sleep
from datetime import datetime
from base64 import b64encode

import psycopg2
import os
import platform

import google.auth.transport.requests
import google.oauth2.id_token


if os.environ.get('SELENIUM_URL') is not None:
    selenium_url = os.environ.get('SELENIUM_URL')
else:
    raise Exception('No remote Selenium webdriver provided in the environment.')

# Overwriting the RemoteConnection class in order to authenticate with the Selenium Webdriver in Cloud Run.
class RemoteConnectionV2(remote_connection.RemoteConnection):
    @classmethod
    def set_remote_connection_authentication_headers(self):
        # Environment variable: identity token -- this can be set locally for debugging purposes.
        if os.environ.get('IDENTITY_TOKEN') is not None:
            print('[Authentication] An identity token was found in the environment. Using it.')
            identity_token = os.environ.get('IDENTITY_TOKEN')
        else:
            print('[Authentication] No identity token was found in the environment. Requesting a new one.')
            auth_req = google.auth.transport.requests.Request()
            identity_token = google.oauth2.id_token.fetch_id_token(auth_req, selenium_url)
        self._auth_header = {'Authorization': 'Bearer %s' % identity_token}
    
    @classmethod
    def get_remote_connection_headers(self, cls, parsed_url, keep_alive=False):
        """
        Get headers for remote request -- an update of Selenium's RemoteConnection to include an Authentication header.
        :Args:
         - parsed_url - The parsed url
         - keep_alive (Boolean) - Is this a keep-alive connection (default: False)
        """

        system = platform.system().lower()
        if system == "darwin": 
            system = "mac"

        default_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'selenium/{} (python {})'.format(__version__, system)
        }

        headers = {**default_headers, **self._auth_header}
        if 'Authorization' not in headers:
            if parsed_url.username:
                base64string = b64encode('{0.username}:{0.password}'.format(parsed_url).encode())
                headers.update({
                    'Authorization': 'Basic {}'.format(base64string.decode())
                })

        if keep_alive:
            headers.update({
                'Connection': 'keep-alive'
            })

        return headers