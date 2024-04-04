from ..node import Node
from src.scripts.uk_electoral_commission import electoral_commission_api
from src.objects.graph_objects.nodes import node_factory

class ElectoralCommissionNode(Node):

    def __init__(self, **kwargs):
        super(ElectoralCommissionNode, self).__init__()
        self.__dict__.update(kwargs)
        self.init_token = self.node_id

    @classmethod
    def batch_init(cls, node_ids):
        raw_results = electoral_commission_api.get_nodes(node_ids)

        ec_types = {ec_type.__name__: ec_type for ec_type in node_factory.ec_nodes_dict.values()}

        nodes = [ec_types[raw_result['node_type']](**raw_result) for raw_result in raw_results]

        return nodes
