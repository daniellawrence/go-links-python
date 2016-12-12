#!/usr/bin/env python
import re

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

go_link_database = {}


class GoRecord(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.url_plain = re.sub('{.*}', '', url)
        self.url_optional = None
        url_optional = re.match('.*{(.*)}.*', url)
        if url_optional:
            self.url_optional = url_optional.groups()[0]

    def __repr__(self):
        return "<GoRecord {.name}>".format(self)

    def link(self, optional=None):
        if optional and self.url_optional:
            optional_args = self.url_optional.replace('^', optional)
            return '{}{}'.format(self.url_plain, optional_args)
        return self.url_plain


@app.route('/')
def index():
    return render_template(
        'index.html',
        go_link_database=go_link_database
    )


@app.route('/<name>')
@app.route('/<name> <optional_argument>')
def redirect_to_link(name, optional_argument=None):
    record = go_link_database.get(name)
    link = record.link(optional_argument)
    return redirect(link)


@app.route('/golinks/edit/<name>/', methods=['GET'])
def golink_edit(name):
    go_record = go_link_database.get(name)
    return render_template(
        'index.html',
        edit_record=go_record,
        go_link_database=go_link_database
    )


@app.route('/golinks/submit', methods=['POST'])
def golink_submit():
    name = request.form.get('name')
    url = request.form.get('url')
    go_record = GoRecord(name, url)
    go_link_database[name] = go_record
    return redirect(url_for('.index'))


if __name__ == '__main__':
    # DEMO GoRecords
    go_link_database['mail'] = GoRecord('mail', 'https://gmail.com')
    go_link_database['git'] = GoRecord('git', 'https://gitlab.com{/search?terms=^}')

    app.debug = True
    app.run(debug=True)
