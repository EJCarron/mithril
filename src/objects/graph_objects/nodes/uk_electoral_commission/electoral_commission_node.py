from ..node import Node
from src.scripts.uk_electoral_commission import electoral_commission_api

class ElectoralCommissionNode(Node):
    @classmethod
    def batch_init(cls, node_ids):
        raw_results = electoral_commission_api.get_nodes(node_ids)

        ec_types = {ec_type.__name__: ec_type for ec_type in cls.__subclasses__()}

        nodes = [ec_types[raw_result['node_type']](**raw_result) for raw_result in raw_results]

        return nodes
