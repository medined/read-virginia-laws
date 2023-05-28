""" Manage getting JSON from a remote service. """

from urllib.error import HTTPError
import json
import logging
import ssl
import time
import urllib.request
from html_cache import HtmlCache

logger = logging.getLogger(__name__)

class JsonFetcher():
    """ Manage getting JSON from remote websites. """

    def __init__(self):
        """ Intialize the object by creating a SSL context. """
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        self.fetch_count = 0
        self.fetch_error = 0
        self.cache_hit_count = 0
        self.cache_miss_count = 0

        self.html_cache = HtmlCache()

    def fetch(self, url):
        """ Get JSON from a URL. """
        self.fetch_count = self.fetch_count + 1

        flag_error, decoded_contents = self.html_cache.read(url)
        if flag_error:
            self.fetch_error = self.fetch_error + 1
            return None

        if decoded_contents:
            self.cache_hit_count = self.cache_hit_count + 1
        else:
            self.cache_miss_count = self.cache_miss_count + 1
            try:
                response = urllib.request.urlopen(url, context=self.context)
                # pause a small amount of time to let the remote server do something else.
                time.sleep(.3)
            except HTTPError:
                logger.fatal('Unable to fetch %s', url)
                self.html_cache.insert(url=url, response='', flag_error=1)
                self.fetch_error = self.fetch_error + 1
                return None

            contents = response.read()
            decoded_contents = contents.decode("utf-8")
            self.html_cache.insert(url=url, response=decoded_contents, flag_error=0)

        json_contents = json.loads(decoded_contents)
        return json_contents
