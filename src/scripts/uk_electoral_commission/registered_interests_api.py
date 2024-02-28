from .. import typesense_client


def find_matches(search_dicts):
    return typesense_client.find_matches(search_dicts)