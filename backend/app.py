#!/usr/bin/env python3

from datetime import datetime
import click
import json

import logging
import logging.config

from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

from ianalyzer import config_fallback as config
from ianalyzer.models import User, Role, db, Corpus
from ianalyzer.factories.app import flask_app 
from ianalyzer.factories.elasticsearch import elasticsearch
from addcorpus.load_corpus import load_corpus
import corpora
from es.es_index import perform_indexing

app = flask_app(config)
migrate = Migrate(app, db)

with open(config.LOG_CONFIG, 'rt') as f:
        log_config = json.load(f)
        logging.config.dictConfig(log_config)

@app.cli.command()
@click.option('--name', '-n', help='Name of superuser', required=True)
@click.option('--pwd', prompt='Please enter password', hide_input=True,
              confirmation_prompt=True, help='Password for superuser.')
def admin(name, pwd):
    ''' Create a superuser with admin rights and access to all corpora.
    If an admin role does not exist yet, it will be created.
    If roles for the defined corpora do not exist yet, they will be created.
    '''
    user = create_user(name, pwd)
    if user == None:
        logging.critical('Superuser with this name already exists.')
        return None

    append_role(user, 'admin', 'Administration role.')

    for corpus in list(config.CORPORA.keys()):
        append_corpus_role(user, corpus)

    return db.session.commit()


@app.cli.command()
@click.option(
    '--corpus', '-c', help='Sets which corpus should be indexed' +
    'If not set, first corpus of CORPORA in config.py will be indexed'
)
@click.option(
    '--start', '-s',
    help='Set the date where indexing should start.' +
    'The input format is YYYY-MM-DD.' +
    'If not set, indexing will start from corpus minimum date.'
)
@click.option(
    '--end', '-e',
    help='Set the date where indexing should end' +
    'The input format is YYYY-MM-DD.' +
    'If not set, indexing will stop at corpus maximum date.'
)
@click.option(
    '--delete', '-d',
    help='Define whether the current index should be deleted' +
    '(turned off by default)'
)
def es(corpus, start, end, delete=False):
    if not corpus:
        corpus = list(config.CORPORA.keys())[0]

    this_corpus = load_corpus(corpus)

    try:
        if start:
            start_index = datetime.strptime(start, '%Y-%m-%d')
        else:
            start_index = this_corpus.min_date

        if end:
            end_index = datetime.strptime(end, '%Y-%m-%d')
        else:
            end_index = this_corpus.max_date

    except Exception:
        logging.critical(
            'Incorrect data format '
            'Example call: flask es -c times -s 1785-01-01 -e 2010-12-31'
        )
        raise

    perform_indexing(corpus, this_corpus, start_index, end_index, delete)


def create_user(name, password=None):
    if User.query.filter_by(username=name).first():
        return None

    password_hash = None if password == None else generate_password_hash(
        password)
    user = User(name, password=password_hash)
    db.session.add(user)
    return user


def append_role(user, name, description):
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name, description)
        db.session.add(role)
    user.role = role
    return role


def append_corpus_role(user, corpus):
    role_corpus = Corpus.query.filter_by(name=corpus).first()
    if not role_corpus:
        role_corpus = Corpus(
            corpus,
            '{0} corpus'.format(corpus)
        )
        db.session.add(role_corpus)
    if role_corpus not in user.role.corpora:
        user.role.corpora.append(role_corpus)


if __name__ == '__main__':
    logging.basicConfig(level=config.LOG_LEVEL)
    app.run()
