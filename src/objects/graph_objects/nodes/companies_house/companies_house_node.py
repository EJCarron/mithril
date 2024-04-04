from ..node import Node


class CompaniesHouseNode(Node):

    def __init__(self, **kwargs):
        super(CompaniesHouseNode, self).__init__()
        self.__dict__.update(kwargs)


    @classmethod
    def batch_init(cls, node_ids):
        nodes = []

        for node_id in node_ids:
            nodes.append(cls.init_from_companies_house_id(node_id))

        return nodes

    @classmethod
    def init_from_companies_house_id(cls, node_id):
        print("SYSTEM ERROR init from node id not implemented")
        return None
