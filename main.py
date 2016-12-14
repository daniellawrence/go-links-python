#!/usr/bin/env python
import re

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import or_
from social.apps.flask_app.routes import social_auth

import settings

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = settings.SECRET_KEY
db = SQLAlchemy(app)

app.register_blueprint(social_auth)


class GoRecord(db.Model):
    __tablename__ = 'gorecord'
    name = db.Column(db.String(50), primary_key=True, unique=True)
    url = db.Column(db.String(255))
    owner = db.Column(db.String(50))

    def __init__(self, name, url, owner=None):
        self.name = name
        self.url = url
        self.owner = owner

    def __repr__(self):
        return "<GoRecord {.name}>".format(self)

    @property
    def favicon(self):
        try:
            domain = self.url_plain.split('/')[2]
            favicon_path = "http://{0}/favicon.ico".format(domain)
            return favicon_path
        except Exception:
            return ''

    @property
    def url_plain(self):
        return re.sub('{.*}', '', self.url)

    def link(self, optional=None):
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


def render_template_with_settings(template, **kwargs):
    return render_template(template, settings=settings, **kwargs)


@app.route('/')
def index():
    return render_template_with_settings(
        'index.html',
        all_records=GoRecord.query.all()
    )


@app.route('/golinks/delete/<name>/')
def golink_delete(name):
    record = GoRecord.query.filter_by(name=name).first()
    db.session.delete(record)
    db.session.commit()

    flash("Successfully deleted '{.name}'".format(record))

    return redirect(url_for('.index'))


@app.route('/<name>')
@app.route('/<name> <optional_argument>')
def redirect_to_link(name, optional_argument=None):
    record = GoRecord.query.filter_by(name=name).first()

    if record is None:
        return redirect(url_for('golink_search', search=name))

    link = record.link(optional_argument)
    return redirect(link)


@app.route('/golinks/edit/<name>/', methods=['GET'])
def golink_edit(name):
    record = GoRecord.query.filter_by(name=name).first_or_404()

    return render_template_with_settings(
        'index.html',
        edit_record=record,
        all_records=GoRecord.query.all()
    )


@app.route('/golinks/search/', methods=['POST'])
def golink_search_redirect_post():
    search = request.form.get('search')
    if not search:
        return redirect(url_for('.index'))

    return redirect(url_for('golink_search', search=search))


@app.route('/golinks/search/<search>/', methods=['GET'])
def golink_search(search):
    search_like = '%{}%'.format(search)
    search_q = GoRecord.query.filter(or_(
        GoRecord.name.like(search_like),
        GoRecord.url.like(search_like),
    ))

    all_records = search_q.all()

    return render_template_with_settings(
        'index.html',
        all_records=all_records,
        previous_search_text=search
    )


@app.route('/golinks/submit/', methods=['POST'])
def golink_submit():
    name = request.form.get('name')
    url = request.form.get('url')

    record = GoRecord.query.filter_by(name=name).first()
    if record:
        record.url = url
        flash("Successfully updated '{.name}'".format(record))
    else:
        record = GoRecord(name, url)
        flash("Successfully created '{.name}'".format(record))

    db.session.add(record)
    db.session.commit()

    return redirect(url_for('.index'))


if __name__ == '__main__':
    db.create_all()

    if settings.ADD_DEMO_RECORDS:
        for name, url in settings.DEMO_RECORDS:

            record = GoRecord(name, url)
            try:
                db.session.add(record)
                db.session.commit()
            except Exception:
                pass

    app.debug = settings.DEBUG
    app.port = settings.PORT
    app.hostname = settings.HOSTNAME
    app.run()
