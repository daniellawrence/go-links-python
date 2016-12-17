""" GoRecord Model that is stored via SQLAlchemny
"""
import re
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class GoRecord(DB.Model):
    """ GoRecord Object """
    __tablename__ = 'gorecord'
    name = DB.Column(DB.String(50), primary_key=True, unique=True)
    url = DB.Column(DB.String(255))
    owner = DB.Column(DB.String(50))

    def __init__(self, name, url, owner=None):
        """ Make a new GoRecord """
        self.name = name
        self.url = url
        self.owner = owner

    def __repr__(self):
        """ Pretty """
        return "<GoRecord {.name}>".format(self)

    @property
    def favicon(self):
        """ Image path for the Favicon of the remote domain """
        domain = self.url_plain.split('/')[2]
        favicon_path = "http://{0}/favicon.ico".format(domain)
        return favicon_path

    @property
    def url_plain(self):
        """ Plain URL without the optional stuff """
        return re.sub('{.*}', '', self.url)

    def link(self, optional=None):
        """ The real link based on the optional stuff """
        url_optional = ''

        try:
            url_optional = re.match('.*{(.*)}.*', self.url)
            url_optional = url_optional.groups()[0]
        except AttributeError:
            url_optional = ''

        if optional:
            optional_args = url_optional.replace('^', optional)
            return '{}{}'.format(self.url_plain, optional_args)

        return self.url_plain
