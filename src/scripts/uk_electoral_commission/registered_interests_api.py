from .. import typesense_client


def find_matches_grouped(search_dicts):
    return typesense_client.find_matches_grouped(search_dicts)

def get_regulated_donee(node_id):
    pass