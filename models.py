from django.db import models
from xml.etree import ElementTree
import requests


class Feed(models.Model):
    label = models.CharField(max_length=50)

    @property
    def feed(self):
        raise NotImplementedError()


class GithubFeed(Feed):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)

    @property
    def headers(self):
        return {'Authorization': 'token {}'.format(self.api_key)}

    @property
    def current_user_request(self):
        url = 'https://github.com/{user}.private.atom?token={token}'.format(
            user=self.username,
            token=self.token
        )
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            raise Exception('Request failed ({}): {}'.format(
                r.status_code, r))
        return r

    @property
    def userfeed_xml(self):
        r = self.current_user_request
        return ElementTree.fromstring(r.text)

    @property
    def feed(self):
        root = self.userfeed_xml
        entries = []
        for entry in root.iter(self.tag('entry')):
            content = entry.find(self.tag('content'))
            entries.append(content.text)
        return entries

    def tag(self, tag_text):
        return '{http://www.w3.org/2005/Atom}' + tag_text

