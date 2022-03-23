#!/usr/bin/env python3

'''
Script to index the data into ElasticSearch.
'''

import sys

from datetime import datetime

import elasticsearch.helpers as es_helpers
from elasticsearch.exceptions import RequestError

from flask import current_app

from ianalyzer.factories.elasticsearch import elasticsearch
from .es_alias import get_new_version_number

import logging
logger = logging.getLogger('indexing')


def create(client, corpus_definition, add, clear, prod):
    '''
    Initialise an ElasticSearch index.
    '''
    if add:
        # we add document to existing index - skip creation.
        return None

    if clear:
        logger.info('Attempting to clean old index...')
        client.indices.delete(
            index=corpus_definition.es_index, ignore=[400, 404])

    settings = corpus_definition.es_settings

    if prod:
        logger.info('Using a versioned index name')
        alias = corpus_definition.es_alias if corpus_definition.es_alias else corpus_definition.es_index
        corpus_definition.es_index = "{}-{}".format(
            corpus_definition.es_index, get_new_version_number(client, alias, corpus_definition.es_index))
        if client.indices.exists(corpus_definition.es_index):
            logger.error('Index `{}` already exists. Do you need to add an alias for it or perhaps delete it?'.format(
                corpus_definition.es_index))
            sys.exit(1)

        logger.info('Adding prod settings to index')
        if not settings.get('index'):
            settings['index'] = {
                'number_of_replicas' : 0,
                'number_of_shards': 5
            }

    logger.info('Attempting to create index `{}`...'.format(
        corpus_definition.es_index))
    try:
        client.indices.create(
            index=corpus_definition.es_index,
            body={
                'settings': settings,
                'mappings': corpus_definition.es_mapping()
            }
        )
    except RequestError as e:
        if not 'already_exists' in e.error:
            # ignore that the index already exist,
            # raise any other errors.
            raise


def populate(client, corpus_name, corpus_definition, start=None, end=None):
    '''
    Populate an ElasticSearch index from the corpus' source files.
    '''

    logger.info('Attempting to populate index...')

    # Obtain source documents
    files = corpus_definition.sources(
        start or corpus_definition.min_date,
        end or corpus_definition.max_date)
    docs = corpus_definition.documents(files)

    # Each source document is decorated as an indexing operation, so that it
    # can be sent to ElasticSearch in bulk
    actions = (
        {
            '_op_type': 'index',
            '_index': corpus_definition.es_index,
            '_id' : doc.get('id'),
            '_source': doc
        } for doc in docs
    )

    corpus_server = current_app.config['SERVERS'][
        current_app.config['CORPUS_SERVER_NAMES'][corpus_name]]
    # Do bulk operation
    response = es_helpers.bulk(
        client,
        actions,
        chunk_size=corpus_server['chunk_size'],
        max_chunk_bytes=corpus_server['max_chunk_bytes'],
        timeout=corpus_server['bulk_timeout'],
        stats_only=True,  # We want to know how many documents were added
    )

    for result in response:
        logger.info('Indexed documents ({}).'.format(result))

    return response


def perform_indexing(corpus_name, corpus_definition, start, end, add, clear, prod):
    logger.info('Started indexing `{}` from {} to {}...'.format(
        corpus_definition.es_index,
        start.strftime('%Y-%m-%d'),
        end.strftime('%Y-%m-%d')
    ))

    # Create and populate the ES index
    client = elasticsearch(corpus_name)
    create(client, corpus_definition, add, clear, prod)
    client.cluster.health(wait_for_status='yellow')
    # import pdb; pdb.set_trace()
    populate(client, corpus_name, corpus_definition, start=start, end=end)

    logger.info('Finished indexing `{}`.'.format(corpus_definition.es_index))

    if prod:
        logger.info('Updating settings for index `{}`'.format(
            corpus_definition.es_index))
        client.indices.put_settings(
            {'number_of_replicas': 1}, corpus_definition.es_index)
