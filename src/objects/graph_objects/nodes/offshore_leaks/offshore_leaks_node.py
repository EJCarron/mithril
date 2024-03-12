from ..node import Node
from .....scripts.OffshoreLeaks import offshore_leaks_api


class OffshoreLeaksNode(Node):

    def __init__(self, **kwargs):
        super(OffshoreLeaksNode, self).__init__()
        self.node_id = 'ol_' + str(kwargs['db_node_id'])
        self.__dict__.update(kwargs)

    @classmethod
    def batch_init(cls, node_ids):
        raw_results = offshore_leaks_api.get_nodes(node_ids)

        ol_types = {ol_type.__name__: ol_type for ol_type in cls.__subclasses__()}

        nodes = [ol_types[raw_result['node_type']](**raw_result) for raw_result in raw_results]

        return nodes




