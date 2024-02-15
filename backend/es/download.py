from django.conf import settings

from ianalyzer.elasticsearch import elasticsearch
from es.search import get_index, search, hits, total_hits

def scroll(corpus, query_model, download_size=None, client=None, **kwargs):
    index = get_index(corpus)
    if not client:
        client = elasticsearch(index)
    server = settings.CORPUS_SERVER_NAMES.get(corpus, 'default')
    scroll_timeout = settings.SERVERS[server]['scroll_timeout']
    scroll_page_size = settings.SERVERS[server]['scroll_page_size']
    size = min(download_size, scroll_page_size) if download_size else scroll_page_size

    output = []
    search_results = client.search(
        index=index,
        size=size,
        scroll=scroll_timeout,
        timeout='60s',
        track_total_hits=True,
        **query_model,
        **kwargs
    )
    output.extend(hits(search_results))
    total = total_hits(search_results)

    if not download_size or download_size > total:
        download_size = total
    num_results = len(hits(search_results))
    scroll_id = search_results['_scroll_id']
    while num_results < download_size:
        search_results = client.scroll(scroll_id=scroll_id,
            scroll=scroll_timeout)
        scroll_id = search_results['_scroll_id']
        num_results += len(hits(search_results))
        output.extend(hits(search_results))
    client.clear_scroll(scroll_id=scroll_id)
    return output, total


def normal_search(corpus, query_model):
    result = search(
        corpus=corpus,
        query_model=query_model
    )
    return hits(result)
