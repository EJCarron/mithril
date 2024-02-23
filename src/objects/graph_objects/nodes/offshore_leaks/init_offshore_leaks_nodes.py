from src.scripts.OffshoreLeaks import offshore_leaks_api
from .. import node_factory


def init_nodes_from_ids(node_ids):
    raw_results = offshore_leaks_api.get_nodes(node_ids)

    nodes = [node_factory.node_dict[raw_result['node_type']](**raw_result) for raw_result in raw_results]

    return nodes


# def determine_node_type_from_raw_result(raw_result):
#     node_type = None
#
#     for type_str, keys_list in node_factory.ol_keys_dict.items():
#         if list(raw_result.keys()) == keys_list:
#             node_type = node_factory.node_dict[type_str]
#             break
#
#     if node_type is None:
#         print('SYSTEM Error raw result keys don\'t match any type. raw result had these keys')
#         for key in raw_result.keys():
#             print(key)
#
#     return node_type
