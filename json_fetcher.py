""" Manage getting JSON from a remote service. """

from urllib.error import HTTPError
import json
import logging
import ssl
import sys
import urllib.request

logger = logging.getLogger(__name__)

class JsonFetcher():
    """ Manage getting JSON from remote websites. """

    def __init__(self):
        """ Intialize the object by creating a SSL context. """
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def fetch(self, url):
        """ Get JSON from a URL. """
        try:
            response = urllib.request.urlopen(url, context=self.context)
        except HTTPError:
            logger.fatal('Unable to fetch %s', url)
            return None
        contents = response.read()
        decoded_contents = contents.decode("utf-8")
        return json.loads(decoded_contents)
