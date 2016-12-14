SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEMO_RECORDS = [
    ('mail', 'https://mail.google.com'),
    ('git', 'https://gitlab.com{/search?terms=^}'),
    ('github', 'https://github.com{/search?terms=^}'),
    ('in', 'https://www.linkedin.com'),
    ('fb', 'https://www.facebook.com')
]

ADD_DEMO_RECORDS = True

TITLE = 'Go Links'
SUB_TITLE = 'Short link service for internal use'

PORT = 5000
HOSTNAME = 'localhost'

DEBUG = True
SECRET_KEY = 'CHANGE_ME'

CREATE_UPDATE_TEXT = 'Save'
SEARCH_TEXT = 'Search'
DELETE_TEXT = 'Delete'
