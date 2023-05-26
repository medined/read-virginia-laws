""" Manage getting JSON from a remote service. """

from urllib.error import HTTPError
import logging
import ssl
import sys
import urllib.request

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class HTMLFetcher():
    """ Manage getting HTML from remote websites. """

    def __init__(self):
        """ Intialize the object by creating a SSL context. """
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def fetch(self, url):
        """ Get HTML from a URL. """
        try:
            response = urllib.request.urlopen(url, context=self.context)
        except HTTPError:
            logger.error('Unable to fetch %s', url)
            return None
        contents = response.read()
        decoded_contents = contents.decode("utf-8")
        return BeautifulSoup(decoded_contents, 'html.parser')
